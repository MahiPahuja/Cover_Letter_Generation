# test_simple_memory.py

from memory_store import SimpleMemory

# Initialize memory
memory = SimpleMemory()
user_id = "test_user"

# Test 1: Add a tone preference
memory.add(user_id, "tone", "professional")
assert memory.query(user_id, "tone") == "professional"
print("✅ Test 1 Passed: Tone set and retrieved correctly.")

# Test 2: Update tone preference
memory.add(user_id, "tone", "enthusiastic")
assert memory.query(user_id, "tone") == "enthusiastic"
print("✅ Test 2 Passed: Tone updated correctly.")

# Test 3: Query missing preference
assert memory.query(user_id, "language") is None
print("✅ Test 3 Passed: Missing preference returns None.")

# Test 4: Add multiple preferences
memory.add(user_id, "language", "English")
memory.add(user_id, "format", "PDF")
assert memory.query(user_id, "language") == "English"
assert memory.query(user_id, "format") == "PDF"
print("✅ Test 4 Passed: Multiple preferences set and retrieved correctly.")

# Debug print of full memory
print("\n[DEBUG] Full memory state:")
for user, prefs in memory.store.items():
    print(f"  User: {user}")
    for key, value in prefs.items():
        print(f"    {key}: {value}")
