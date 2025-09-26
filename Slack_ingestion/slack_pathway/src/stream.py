import json
import logging
from pathlib import Path
from typing import Generator, Dict, Any
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STREAM_FILE = Path("messages.json")

def push_message(msg: Dict[str, Any]) -> None:
    """Push a new message to the stream (file-based for Pathway integration)."""
    try:
        STREAM_FILE.touch(exist_ok=True)
        
        # Add timestamp if not present
        if 'ts' not in msg or not msg['ts']:
            msg['ts'] = str(time.time())
        
        # Add message_id if not present
        if 'message_id' not in msg or not msg['message_id']:
            msg['message_id'] = f"{msg.get('ts', '')}_{msg.get('user', 'unknown')}"
        
        # Write to file
        with STREAM_FILE.open("a") as f:
            f.write(json.dumps(msg) + "\n")
        
        logger.info(f"✅ Message pushed to stream: {msg.get('user', 'unknown')} - {msg.get('text', '')[:50]}...")
        
    except Exception as e:
        logger.error(f"❌ Error pushing message to stream: {e}")

def read_stream() -> Generator[Dict[str, Any], None, None]:
    """Yield messages from the stream for Pathway consumption."""
    try:
        if not STREAM_FILE.exists():
            logger.info("📁 No messages file found, waiting for messages...")
            return
        
        with STREAM_FILE.open() as f:
            for line_num, line in enumerate(f, 1):
                try:
                    if line.strip():
                        msg = json.loads(line.strip())
                        yield msg
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ Skipping invalid JSON on line {line_num}: {e}")
                    continue
                    
    except Exception as e:
        logger.error(f"❌ Error reading from stream: {e}")

def get_stream_stats() -> Dict[str, Any]:
    """Get statistics about the message stream."""
    try:
        if not STREAM_FILE.exists():
            return {"total_messages": 0, "file_size": 0}
        
        message_count = 0
        with STREAM_FILE.open() as f:
            for line in f:
                if line.strip():
                    message_count += 1
        
        return {
            "total_messages": message_count,
            "file_size": STREAM_FILE.stat().st_size,
            "file_path": str(STREAM_FILE)
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting stream stats: {e}")
        return {"error": str(e)}
