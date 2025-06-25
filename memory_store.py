from autogen_core.memory import ListMemory, MemoryContent, MemoryMimeType

# Default user ID used across the app
user_id = "default_user"

# Initialize ListMemory instance to store preferences like tone
tone_memory = ListMemory()

#  Function to set tone in memory
async def set_tone(user_id: str, tone: str):
    await tone_memory.add(
        MemoryContent(
            content=tone,  # just the tone string like "formal", "professional", etc.
            mime_type=MemoryMimeType.TEXT,
            metadata={"user_id": user_id}
        )
    )

#  Function to get tone from memory
async def get_tone(user_id: str):
    memory_items = await tone_memory.query(metadata={"user_id": user_id})
    return memory_items[-1].content if memory_items else "professional"  # fallback default
