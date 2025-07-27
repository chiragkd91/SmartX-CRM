"""
Performance Optimization Module for CRM Application
Handles database optimization, caching, image optimization, code minification, and monitoring
"""

import os
import sys
import time
import logging
import psutil
import sqlite3
import hashlib
import json
import gzip
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import wraps
import threading
from datetime import datetime, timedelta
import redis
from PIL import Image
import requests
from flask import Flask, request, g, current_app
import psycopg2
from psycopg2.extras import RealDictCursor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor application performance metrics"""
    
    def __init__(self):
        self.metrics = {
            'response_times': [],
            'memory_usage': [],
            'cpu_usage': [],
            'database_queries': [],
            'cache_hits': 0,
            'cache_misses': 0,
            'errors': []
        }
        self.start_time = time.time()
        self.lock = threading.Lock()
    
    def record_response_time(self, endpoint: str, method: str, duration: float):
        """Record response time for an endpoint"""
        with self.lock:
            self.metrics['response_times'].append({
                'endpoint': endpoint,
                'method': method,
                'duration': duration,
                'timestamp': datetime.now()
            })
    
    def record_database_query(self, query: str, duration: float):
        """Record database query performance"""
        with self.lock:
            self.metrics['database_queries'].append({
                'query': query,
                'duration': duration,
                'timestamp': datetime.now()
            })
    
    def record_cache_hit(self):
        """Record cache hit"""
        with self.lock:
            self.metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Record cache miss"""
        with self.lock:
            self.metrics['cache_misses'] += 1
    
    def record_error(self, error: str, endpoint: str = None):
        """Record application error"""
        with self.lock:
            self.metrics['errors'].append({
                'error': error,
                'endpoint': endpoint,
                'timestamp': datetime.now()
            })
    
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        with self.lock:
            uptime = time.time() - self.start_time
            
            # Calculate average response time
            if self.metrics['response_times']:
                avg_response_time = sum(r['duration'] for r in self.metrics['response_times']) / len(self.metrics['response_times'])
            else:
                avg_response_time = 0
            
            # Calculate cache hit rate
            total_cache_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
            cache_hit_rate = (self.metrics['cache_hits'] / total_cache_requests * 100) if total_cache_requests > 0 else 0
            
            # Get system metrics
            memory_usage = psutil.virtual_memory().percent
            cpu_usage = psutil.cpu_percent()
            
            return {
                'uptime_seconds': uptime,
                'average_response_time': avg_response_time,
                'cache_hit_rate': cache_hit_rate,
                'total_requests': len(self.metrics['response_times']),
                'total_errors': len(self.metrics['errors']),
                'memory_usage_percent': memory_usage,
                'cpu_usage_percent': cpu_usage,
                'slowest_endpoints': self.get_slowest_endpoints(),
                'most_frequent_queries': self.get_most_frequent_queries(),
                'recent_errors': self.metrics['errors'][-10:]  # Last 10 errors
            }
    
    def get_slowest_endpoints(self, limit: int = 5) -> List[Dict]:
        """Get slowest endpoints"""
        if not self.metrics['response_times']:
            return []
        
        endpoint_times = {}
        for record in self.metrics['response_times']:
            key = f"{record['method']} {record['endpoint']}"
            if key not in endpoint_times:
                endpoint_times[key] = []
            endpoint_times[key].append(record['duration'])
        
        slowest = []
        for endpoint, times in endpoint_times.items():
            avg_time = sum(times) / len(times)
            slowest.append({
                'endpoint': endpoint,
                'average_time': avg_time,
                'request_count': len(times)
            })
        
        return sorted(slowest, key=lambda x: x['average_time'], reverse=True)[:limit]
    
    def get_most_frequent_queries(self, limit: int = 5) -> List[Dict]:
        """Get most frequent database queries"""
        if not self.metrics['database_queries']:
            return []
        
        query_counts = {}
        for record in self.metrics['database_queries']:
            query = record['query'][:50] + '...' if len(record['query']) > 50 else record['query']
            if query not in query_counts:
                query_counts[query] = {'count': 0, 'total_time': 0}
            query_counts[query]['count'] += 1
            query_counts[query]['total_time'] += record['duration']
        
        frequent = []
        for query, data in query_counts.items():
            frequent.append({
                'query': query,
                'count': data['count'],
                'average_time': data['total_time'] / data['count']
            })
        
        return sorted(frequent, key=lambda x: x['count'], reverse=True)[:limit]

class DatabaseOptimizer:
    """Optimize database performance"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connection = None
    
    def connect(self):
        """Connect to database"""
        try:
            if self.db_url.startswith('sqlite'):
                self.connection = sqlite3.connect(self.db_url.replace('sqlite:///', ''))
            else:
                self.connection = psycopg2.connect(self.db_url)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def analyze_tables(self) -> Dict:
        """Analyze table performance"""
        if not self.connection:
            self.connect()
        
        analysis = {}
        
        try:
            if isinstance(self.connection, sqlite3.Connection):
                # SQLite analysis
                cursor = self.connection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    
                    analysis[table_name] = {
                        'columns': len(columns),
                        'row_count': row_count,
                        'indexes': self.get_sqlite_indexes(table_name)
                    }
            else:
                # PostgreSQL analysis
                cursor = self.connection.cursor(cursor_factory=RealDictCursor)
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        attname,
                        n_distinct,
                        correlation
                    FROM pg_stats 
                    WHERE schemaname = 'public'
                """)
                stats = cursor.fetchall()
                
                for stat in stats:
                    table_name = stat['tablename']
                    if table_name not in analysis:
                        analysis[table_name] = {
                            'columns': [],
                            'row_count': 0,
                            'indexes': []
                        }
                    
                    analysis[table_name]['columns'].append({
                        'name': stat['attname'],
                        'distinct_values': stat['n_distinct'],
                        'correlation': stat['correlation']
                    })
                
                # Get row counts
                for table_name in analysis.keys():
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    analysis[table_name]['row_count'] = cursor.fetchone()[0]
                
                # Get indexes
                for table_name in analysis.keys():
                    analysis[table_name]['indexes'] = self.get_postgresql_indexes(table_name)
        
        except Exception as e:
            logger.error(f"Table analysis failed: {e}")
        
        return analysis
    
    def get_sqlite_indexes(self, table_name: str) -> List[str]:
        """Get SQLite indexes for a table"""
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = cursor.fetchall()
        return [index[1] for index in indexes]
    
    def get_postgresql_indexes(self, table_name: str) -> List[Dict]:
        """Get PostgreSQL indexes for a table"""
        cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                indexname,
                indexdef
            FROM pg_indexes 
            WHERE tablename = %s
        """, (table_name,))
        indexes = cursor.fetchall()
        return [{'name': idx['indexname'], 'definition': idx['indexdef']} for idx in indexes]
    
    def optimize_queries(self) -> List[str]:
        """Generate query optimization recommendations"""
        recommendations = []
        
        try:
            if isinstance(self.connection, sqlite3.Connection):
                # SQLite optimizations
                cursor = self.connection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    
                    # Check for missing indexes on common query columns
                    for column in columns:
                        if column[1] in ['email', 'phone', 'created_at', 'updated_at', 'status']:
                            recommendations.append(
                                f"Consider adding index on {table_name}.{column[1]} for better query performance"
                            )
            else:
                # PostgreSQL optimizations
                cursor = self.connection.cursor(cursor_factory=RealDictCursor)
                
                # Check for missing indexes
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        attname,
                        n_distinct
                    FROM pg_stats 
                    WHERE schemaname = 'public' 
                    AND n_distinct > 100
                    AND attname IN ('email', 'phone', 'created_at', 'updated_at', 'status')
                """)
                
                for stat in cursor.fetchall():
                    recommendations.append(
                        f"Consider adding index on {stat['tablename']}.{stat['attname']} "
                        f"(distinct values: {stat['n_distinct']})"
                    )
                
                # Check for table bloat
                cursor.execute("""
                    SELECT 
                        schemaname,
                        tablename,
                        n_tup_ins,
                        n_tup_upd,
                        n_tup_del,
                        n_live_tup,
                        n_dead_tup
                    FROM pg_stat_user_tables
                    WHERE n_dead_tup > n_live_tup * 0.1
                """)
                
                for table in cursor.fetchall():
                    recommendations.append(
                        f"Table {table['tablename']} has high bloat "
                        f"({table['n_dead_tup']} dead tuples). Consider VACUUM."
                    )
        
        except Exception as e:
            logger.error(f"Query optimization analysis failed: {e}")
        
        return recommendations
    
    def create_indexes(self, indexes: List[Tuple[str, str, str]]):
        """Create recommended indexes"""
        if not self.connection:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            
            for table, column, index_name in indexes:
                try:
                    cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table} ({column})")
                    logger.info(f"Created index {index_name} on {table}.{column}")
                except Exception as e:
                    logger.error(f"Failed to create index {index_name}: {e}")
            
            self.connection.commit()
            
        except Exception as e:
            logger.error(f"Index creation failed: {e}")
    
    def vacuum_database(self):
        """Vacuum database to reclaim space"""
        if not self.connection:
            self.connect()
        
        try:
            cursor = self.connection.cursor()
            
            if isinstance(self.connection, sqlite3.Connection):
                cursor.execute("VACUUM")
            else:
                cursor.execute("VACUUM ANALYZE")
            
            logger.info("Database vacuum completed")
            
        except Exception as e:
            logger.error(f"Database vacuum failed: {e}")

class CacheManager:
    """Manage application caching"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.redis_client = None
        self.monitor = PerformanceMonitor()
    
    def connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = redis.from_url(self.redis_url)
            self.redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.redis_client = None
    
    def get(self, key: str, default=None):
        """Get value from cache"""
        if not self.redis_client:
            self.connect()
        
        try:
            value = self.redis_client.get(key)
            if value is not None:
                self.monitor.record_cache_hit()
                return json.loads(value)
            else:
                self.monitor.record_cache_miss()
                return default
        except Exception as e:
            logger.error(f"Cache get failed for key {key}: {e}")
            return default
    
    def set(self, key: str, value, expire: int = 3600):
        """Set value in cache"""
        if not self.redis_client:
            self.connect()
        
        try:
            serialized_value = json.dumps(value)
            self.redis_client.setex(key, expire, serialized_value)
            return True
        except Exception as e:
            logger.error(f"Cache set failed for key {key}: {e}")
            return False
    
    def delete(self, key: str):
        """Delete value from cache"""
        if not self.redis_client:
            self.connect()
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete failed for key {key}: {e}")
            return False
    
    def clear_pattern(self, pattern: str):
        """Clear cache entries matching pattern"""
        if not self.redis_client:
            self.connect()
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"Cleared {len(keys)} cache entries matching pattern: {pattern}")
            return True
        except Exception as e:
            logger.error(f"Cache clear pattern failed: {e}")
            return False
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        if not self.redis_client:
            self.connect()
        
        try:
            info = self.redis_client.info()
            return {
                'total_connections_received': info.get('total_connections_received', 0),
                'total_commands_processed': info.get('total_commands_processed', 0),
                'keyspace_hits': info.get('keyspace_hits', 0),
                'keyspace_misses': info.get('keyspace_misses', 0),
                'used_memory_human': info.get('used_memory_human', '0B'),
                'connected_clients': info.get('connected_clients', 0),
                'uptime_in_seconds': info.get('uptime_in_seconds', 0)
            }
        except Exception as e:
            logger.error(f"Cache stats failed: {e}")
            return {}

class ImageOptimizer:
    """Optimize images for web delivery"""
    
    def __init__(self, quality: int = 85, max_width: int = 1920):
        self.quality = quality
        self.max_width = max_width
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp']
    
    def optimize_image(self, input_path: str, output_path: str = None) -> str:
        """Optimize a single image"""
        if output_path is None:
            output_path = input_path
        
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize if too large
                if img.width > self.max_width:
                    ratio = self.max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((self.max_width, new_height), Image.LANCZOS)
                
                # Save optimized image
                img.save(output_path, 'JPEG', quality=self.quality, optimize=True)
                
                # Get file sizes
                original_size = os.path.getsize(input_path)
                optimized_size = os.path.getsize(output_path)
                savings = ((original_size - optimized_size) / original_size) * 100
                
                logger.info(f"Optimized {input_path}: {original_size} -> {optimized_size} bytes ({savings:.1f}% savings)")
                
                return output_path
                
        except Exception as e:
            logger.error(f"Image optimization failed for {input_path}: {e}")
            return input_path
    
    def optimize_directory(self, directory: str, recursive: bool = True):
        """Optimize all images in a directory"""
        directory_path = Path(directory)
        
        if recursive:
            image_files = list(directory_path.rglob('*'))
        else:
            image_files = list(directory_path.glob('*'))
        
        image_files = [f for f in image_files if f.suffix.lower() in self.supported_formats]
        
        logger.info(f"Found {len(image_files)} images to optimize")
        
        for image_file in image_files:
            self.optimize_image(str(image_file))
    
    def create_webp_versions(self, directory: str):
        """Create WebP versions of images for better compression"""
        directory_path = Path(directory)
        image_files = list(directory_path.rglob('*.jpg')) + list(directory_path.rglob('*.jpeg')) + list(directory_path.rglob('*.png'))
        
        for image_file in image_files:
            try:
                webp_path = image_file.with_suffix('.webp')
                
                with Image.open(image_file) as img:
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    img.save(webp_path, 'WEBP', quality=self.quality)
                    
                    original_size = os.path.getsize(image_file)
                    webp_size = os.path.getsize(webp_path)
                    savings = ((original_size - webp_size) / original_size) * 100
                    
                    logger.info(f"Created WebP version: {webp_path} ({savings:.1f}% smaller)")
                    
            except Exception as e:
                logger.error(f"WebP conversion failed for {image_file}: {e}")

class CodeOptimizer:
    """Optimize code for production"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.static_dir = self.project_root / 'static'
        self.templates_dir = self.project_root / 'templates'
    
    def minify_css(self, input_file: str, output_file: str = None):
        """Minify CSS file"""
        if output_file is None:
            output_file = input_file
        
        try:
            with open(input_file, 'r') as f:
                css_content = f.read()
            
            # Basic CSS minification
            import re
            
            # Remove comments
            css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
            
            # Remove unnecessary whitespace
            css_content = re.sub(r'\s+', ' ', css_content)
            css_content = re.sub(r';\s*}', '}', css_content)
            css_content = re.sub(r'{\s*', '{', css_content)
            css_content = re.sub(r'}\s*', '}', css_content)
            css_content = re.sub(r':\s*', ':', css_content)
            css_content = re.sub(r';\s*', ';', css_content)
            
            # Remove trailing semicolons
            css_content = re.sub(r';}', '}', css_content)
            
            with open(output_file, 'w') as f:
                f.write(css_content.strip())
            
            logger.info(f"Minified CSS: {input_file} -> {output_file}")
            
        except Exception as e:
            logger.error(f"CSS minification failed for {input_file}: {e}")
    
    def minify_js(self, input_file: str, output_file: str = None):
        """Minify JavaScript file"""
        if output_file is None:
            output_file = input_file
        
        try:
            with open(input_file, 'r') as f:
                js_content = f.read()
            
            # Basic JavaScript minification
            import re
            
            # Remove single-line comments
            js_content = re.sub(r'//.*$', '', js_content, flags=re.MULTILINE)
            
            # Remove multi-line comments
            js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
            
            # Remove unnecessary whitespace
            js_content = re.sub(r'\s+', ' ', js_content)
            js_content = re.sub(r';\s*}', '}', js_content)
            js_content = re.sub(r'{\s*', '{', js_content)
            js_content = re.sub(r'}\s*', '}', js_content)
            
            with open(output_file, 'w') as f:
                f.write(js_content.strip())
            
            logger.info(f"Minified JavaScript: {input_file} -> {output_file}")
            
        except Exception as e:
            logger.error(f"JavaScript minification failed for {input_file}: {e}")
    
    def compress_static_files(self):
        """Compress static files with gzip"""
        static_files = []
        
        if self.static_dir.exists():
            static_files.extend(list(self.static_dir.rglob('*.css')))
            static_files.extend(list(self.static_dir.rglob('*.js')))
            static_files.extend(list(self.static_dir.rglob('*.html')))
        
        for file_path in static_files:
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                compressed_content = gzip.compress(content)
                gzip_path = file_path.with_suffix(file_path.suffix + '.gz')
                
                with open(gzip_path, 'wb') as f:
                    f.write(compressed_content)
                
                original_size = len(content)
                compressed_size = len(compressed_content)
                compression_ratio = (1 - compressed_size / original_size) * 100
                
                logger.info(f"Compressed {file_path}: {original_size} -> {compressed_size} bytes ({compression_ratio:.1f}% compression)")
                
            except Exception as e:
                logger.error(f"File compression failed for {file_path}: {e}")
    
    def optimize_all(self):
        """Run all code optimizations"""
        logger.info("Starting code optimization...")
        
        # Minify CSS files
        css_files = list(self.static_dir.rglob('*.css')) if self.static_dir.exists() else []
        for css_file in css_files:
            self.minify_css(str(css_file))
        
        # Minify JavaScript files
        js_files = list(self.static_dir.rglob('*.js')) if self.static_dir.exists() else []
        for js_file in js_files:
            self.minify_js(str(js_file))
        
        # Compress static files
        self.compress_static_files()
        
        logger.info("Code optimization completed")

def performance_decorator(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            
            # Record performance if monitor is available
            if hasattr(current_app, 'performance_monitor'):
                current_app.performance_monitor.record_response_time(
                    request.endpoint, request.method, duration
                )
            
            return result
        except Exception as e:
            duration = time.time() - start_time
            
            # Record error if monitor is available
            if hasattr(current_app, 'performance_monitor'):
                current_app.performance_monitor.record_error(str(e), request.endpoint)
            
            raise
    
    return wrapper

def cache_decorator(expire: int = 3600, key_prefix: str = ""):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            if hasattr(current_app, 'cache_manager'):
                cached_result = current_app.cache_manager.get(cache_key)
                if cached_result is not None:
                    return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            
            if hasattr(current_app, 'cache_manager'):
                current_app.cache_manager.set(cache_key, result, expire)
            
            return result
        return wrapper
    return decorator

def optimize_flask_app(app: Flask, db_url: str, redis_url: str = "redis://localhost:6379/0"):
    """Optimize Flask application"""
    
    # Initialize performance monitoring
    app.performance_monitor = PerformanceMonitor()
    
    # Initialize cache manager
    app.cache_manager = CacheManager(redis_url)
    
    # Initialize database optimizer
    app.db_optimizer = DatabaseOptimizer(db_url)
    
    # Add performance monitoring middleware
    @app.before_request
    def before_request():
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            app.performance_monitor.record_response_time(
                request.endpoint, request.method, duration
            )
        return response
    
    # Add performance endpoint
    @app.route('/api/performance')
    def performance_metrics():
        return json.dumps(app.performance_monitor.get_performance_report(), indent=2)
    
    # Add cache stats endpoint
    @app.route('/api/cache/stats')
    def cache_stats():
        return json.dumps(app.cache_manager.get_cache_stats(), indent=2)
    
    logger.info("Flask application optimized with performance monitoring and caching")

def main():
    """Main optimization function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CRM Performance Optimizer')
    parser.add_argument('--db-url', required=True, help='Database URL')
    parser.add_argument('--redis-url', default='redis://localhost:6379/0', help='Redis URL')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--optimize-db', action='store_true', help='Optimize database')
    parser.add_argument('--optimize-images', action='store_true', help='Optimize images')
    parser.add_argument('--optimize-code', action='store_true', help='Optimize code')
    parser.add_argument('--cache-stats', action='store_true', help='Show cache statistics')
    
    args = parser.parse_args()
    
    if args.optimize_db:
        logger.info("Starting database optimization...")
        db_optimizer = DatabaseOptimizer(args.db_url)
        db_optimizer.connect()
        
        analysis = db_optimizer.analyze_tables()
        logger.info("Database analysis completed")
        
        recommendations = db_optimizer.optimize_queries()
        for rec in recommendations:
            logger.info(f"Recommendation: {rec}")
        
        db_optimizer.vacuum_database()
    
    if args.optimize_images:
        logger.info("Starting image optimization...")
        image_optimizer = ImageOptimizer()
        image_optimizer.optimize_directory(args.project_root)
        image_optimizer.create_webp_versions(args.project_root)
    
    if args.optimize_code:
        logger.info("Starting code optimization...")
        code_optimizer = CodeOptimizer(args.project_root)
        code_optimizer.optimize_all()
    
    if args.cache_stats:
        logger.info("Cache statistics:")
        cache_manager = CacheManager(args.redis_url)
        stats = cache_manager.get_cache_stats()
        for key, value in stats.items():
            logger.info(f"{key}: {value}")

if __name__ == "__main__":
    main() 