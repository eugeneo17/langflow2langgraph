from generated_loop_graph import create_graph

def test_loop_graph():
    # Create the graph
    app = create_graph()
    
    # Test with a comma-separated list
    test_input = {
        "input": "apple,banana,cherry,date"
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

if __name__ == "__main__":
    print("=== Testing Loop Graph ===\n")
    test_loop_graph()
