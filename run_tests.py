#!/usr/bin/env python3
"""
Test runner script for CRM application
Usage: python run_tests.py [options]
"""

import sys
import subprocess
import argparse
import os

def run_command(command):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        return result.returncode, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout, e.stderr

def main():
    parser = argparse.ArgumentParser(description='Run CRM application tests')
    parser.add_argument('--unit', action='store_true', 
                       help='Run unit tests only')
    parser.add_argument('--integration', action='store_true', 
                       help='Run integration tests only')
    parser.add_argument('--api', action='store_true', 
                       help='Run API tests only')
    parser.add_argument('--security', action='store_true', 
                       help='Run security tests only')
    parser.add_argument('--coverage', action='store_true', 
                       help='Run tests with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Verbose output')
    parser.add_argument('--fast', action='store_true', 
                       help='Skip slow tests')
    parser.add_argument('--file', type=str, 
                       help='Run tests from specific file')
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest']
    
    if args.verbose:
        cmd.append('-v')
    
    if args.coverage:
        cmd.extend(['--cov=app', '--cov-report=html', '--cov-report=term'])
    
    if args.fast:
        cmd.append('-m "not slow"')
    
    if args.unit:
        cmd.append('-m unit')
    elif args.integration:
        cmd.append('-m integration')
    elif args.api:
        cmd.append('-m api')
    elif args.security:
        cmd.append('-m security')
    elif args.file:
        cmd.append(args.file)
    else:
        # Run all tests by default
        pass
    
    # Add test directory
    cmd.append('tests/')
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 50)
    
    # Run the tests
    returncode, stdout, stderr = run_command(' '.join(cmd))
    
    # Print output
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)
    
    print("=" * 50)
    
    if returncode == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(returncode)

if __name__ == '__main__':
    main() 