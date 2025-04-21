from generated_conditional_graph import create_graph

def test_conditional_graph():
    # Create the graph
    app = create_graph()
    
    # Test with different inputs
    test_cases = [
        {"input": "How are you doing today?"},
        {"input": "I'm feeling great about this project!"},
        {"input": "I'm really disappointed with the results."},
        {"input": "The weather is cloudy today."}
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\nTest Case {i}")
        print("-" * 40)
        print("Input:", test_input)
        
        try:
            result = app.invoke(test_input)
            print("Output:", result)
            print("Status: Success ✅")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Status: Failed ❌")

if __name__ == "__main__":
    print("=== Testing Conditional Graph ===\n")
    test_conditional_graph()
