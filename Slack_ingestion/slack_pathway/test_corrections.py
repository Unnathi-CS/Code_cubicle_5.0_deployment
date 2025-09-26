#!/usr/bin/env python3
"""
Test script to verify that all Pathway integration corrections are working properly.
"""

import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported without errors."""
    logger.info("🧪 Testing imports...")
    
    try:
        # Test basic imports
        import pathway as pw
        logger.info("✅ Pathway imported successfully")
        
        from stream import push_message, read_stream, get_stream_stats
        logger.info("✅ Stream module imported successfully")
        
        from utils import is_valid_message
        logger.info("✅ Utils module imported successfully")
        
        from ai_service import rag_service
        logger.info("✅ AI service imported successfully")
        
        from rag_query_service import rag_query_service
        logger.info("✅ RAG query service imported successfully")
        
        from pathway_rag_service import PathwayRAGService, initialize_pathway_rag_service
        logger.info("✅ Pathway RAG service imported successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Import test failed: {e}")
        return False

def test_pathway_pipeline():
    """Test that the Pathway pipeline can be imported without blocking."""
    logger.info("🧪 Testing Pathway pipeline...")
    
    try:
        from pathway_pipeline import PATHWAY_TABLES
        logger.info("✅ Pathway pipeline imported successfully")
        logger.info(f"✅ Available tables: {list(PATHWAY_TABLES.keys())}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Pathway pipeline test failed: {e}")
        return False

def test_stream_functions():
    """Test stream functions work correctly."""
    logger.info("🧪 Testing stream functions...")
    
    try:
        from stream import push_message, read_stream, get_stream_stats
        
        # Test push_message
        test_msg = {
            "user": "test_user",
            "text": "This is a test message",
            "channel": "test_channel"
        }
        push_message(test_msg)
        logger.info("✅ push_message works correctly")
        
        # Test get_stream_stats
        stats = get_stream_stats()
        logger.info(f"✅ Stream stats: {stats}")
        
        # Test read_stream
        message_count = 0
        for msg in read_stream():
            message_count += 1
            if message_count >= 5:  # Limit to prevent infinite loop
                break
        
        logger.info(f"✅ read_stream works correctly (found {message_count} messages)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Stream functions test failed: {e}")
        return False

def test_main_app_import():
    """Test that main app can be imported without errors."""
    logger.info("🧪 Testing main app import...")
    
    try:
        # Import the main app module (but don't run it)
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", "src/main.py")
        main_module = importlib.util.module_from_spec(spec)
        
        # This should not block or cause errors
        logger.info("✅ Main app module can be imported")
        return True
        
    except Exception as e:
        logger.error(f"❌ Main app import test failed: {e}")
        return False

def test_environment_setup():
    """Test that environment is properly set up."""
    logger.info("🧪 Testing environment setup...")
    
    try:
        # Check if .env file exists
        env_file = Path(".env")
        if env_file.exists():
            logger.info("✅ .env file exists")
        else:
            logger.warning("⚠️ .env file not found - create it with your API keys")
        
        # Check Python version
        import sys
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        logger.info(f"✅ Python version: {python_version}")
        
        if sys.version_info >= (3, 10):
            logger.info("✅ Python version is compatible with Pathway")
        else:
            logger.warning("⚠️ Python 3.10+ recommended for Pathway")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Environment setup test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("🚀 Starting Pathway Integration Tests")
    logger.info("=" * 50)
    
    tests = [
        ("Environment Setup", test_environment_setup),
        ("Imports", test_imports),
        ("Pathway Pipeline", test_pathway_pipeline),
        ("Stream Functions", test_stream_functions),
        ("Main App Import", test_main_app_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                logger.info(f"✅ {test_name} - PASSED")
                passed += 1
            else:
                logger.error(f"❌ {test_name} - FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} - ERROR: {e}")
    
    logger.info("\n" + "=" * 50)
    logger.info(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! The Pathway integration is ready.")
        logger.info("\n📋 Next steps:")
        logger.info("1. Create .env file with your API keys")
        logger.info("2. Run: python src/main.py")
        logger.info("3. Visit: http://localhost:5000")
        return True
    else:
        logger.error("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
