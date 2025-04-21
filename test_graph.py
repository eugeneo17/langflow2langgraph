from generated_graph import create_graph

def test_simple_input():
    # Create the graph
    app = create_graph()
    
    # Test with a simple input
    test_input = {
        "input": "This is a test message that needs to be processed."
    }
    
    print("Input:", test_input)
    print("\nProcessing...\n")
    
    try:
        # Run the graph
        result = app.invoke(test_input)
        print("Output:", result)
        print("\nStatus: Success ✅")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nStatus: Failed ❌")

def test_multiple_inputs():
    app = create_graph()
    
    # Test with multiple different inputs
    test_cases = [
        {"input": "Short test."},
        {"input": "A longer test message that contains multiple words and should be processed."},
        {"input": ""},  # Empty input to test error handling
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
    print("=== Testing Generated Graph ===\n")
    
    print("Test 1: Simple Input")
    print("-" * 40)
    test_simple_input()
    
    print("\nTest 2: Multiple Inputs")
    print("-" * 40)
    test_multiple_inputs()