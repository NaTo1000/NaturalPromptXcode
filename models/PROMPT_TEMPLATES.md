# Prompt Templates

This document contains prompt templates used for generating iOS applications.

## System Prompts

### General iOS Development
```
You are an expert iOS developer with deep knowledge of Swift, SwiftUI, UIKit,
and iOS application architecture. You write clean, efficient, and well-documented
code following Apple's best practices and Human Interface Guidelines.

When generating code:
1. Use modern Swift features and syntax
2. Follow Swift naming conventions
3. Include proper error handling
4. Write clear, concise comments
5. Follow the Single Responsibility Principle
6. Use appropriate design patterns
```

### SwiftUI Specialist
```
You are a SwiftUI expert. Generate modern, declarative SwiftUI code that is:
- Performant and efficient
- Follows SwiftUI best practices
- Uses proper state management (@State, @Binding, @ObservedObject)
- Implements proper view composition
- Handles edge cases gracefully
```

### UIKit Specialist
```
You are a UIKit expert. Generate UIKit code that:
- Properly manages view lifecycle
- Uses Auto Layout correctly
- Implements proper memory management
- Follows MVC or MVVM patterns
- Handles orientation changes appropriately
```

## Task-Specific Prompts

### Simple UI Generation
```
Create a {framework} view for an iOS app with the following features:
{features}

Requirements:
- Use iOS {ios_version} APIs
- Follow Apple Human Interface Guidelines
- Include proper accessibility support
- Handle dark mode appropriately
```

### Data-Driven App
```
Create an iOS app that manages {data_type} with the following capabilities:
{capabilities}

Implementation requirements:
- Use {persistence_method} for data persistence
- Implement proper CRUD operations
- Include data validation
- Handle errors gracefully
- Support offline usage
```

### Network-Based App
```
Create an iOS app that fetches {data_type} from {api_type}:
{requirements}

Technical requirements:
- Use URLSession or async/await
- Implement proper error handling
- Show loading states
- Cache responses appropriately
- Handle network errors
```

## Few-Shot Examples

### Example 1: Counter App
**Prompt:**
```
Create a simple counter app with increment and decrement buttons
```

**Expected Output:**
```swift
import SwiftUI

struct ContentView: View {
    @State private var count = 0
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Counter: \(count)")
                .font(.largeTitle)
                .fontWeight(.bold)
            
            HStack(spacing: 20) {
                Button(action: { count -= 1 }) {
                    Image(systemName: "minus.circle.fill")
                        .font(.system(size: 50))
                }
                
                Button(action: { count += 1 }) {
                    Image(systemName: "plus.circle.fill")
                        .font(.system(size: 50))
                }
            }
        }
        .padding()
    }
}
```

### Example 2: Todo List
**Prompt:**
```
Create a todo list app where users can add, complete, and delete tasks
```

**Expected Output:**
```swift
import SwiftUI

struct TodoItem: Identifiable {
    let id = UUID()
    var title: String
    var isCompleted: Bool
}

struct ContentView: View {
    @State private var todos: [TodoItem] = []
    @State private var newTodoTitle = ""
    
    var body: some View {
        NavigationView {
            VStack {
                HStack {
                    TextField("New task", text: $newTodoTitle)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    
                    Button("Add") {
                        addTodo()
                    }
                    .disabled(newTodoTitle.isEmpty)
                }
                .padding()
                
                List {
                    ForEach(todos) { todo in
                        HStack {
                            Image(systemName: todo.isCompleted ? "checkmark.circle.fill" : "circle")
                                .foregroundColor(todo.isCompleted ? .green : .gray)
                                .onTapGesture {
                                    toggleTodo(todo)
                                }
                            
                            Text(todo.title)
                                .strikethrough(todo.isCompleted)
                            
                            Spacer()
                        }
                    }
                    .onDelete(perform: deleteTodo)
                }
            }
            .navigationTitle("Todo List")
        }
    }
    
    private func addTodo() {
        let todo = TodoItem(title: newTodoTitle, isCompleted: false)
        todos.append(todo)
        newTodoTitle = ""
    }
    
    private func toggleTodo(_ todo: TodoItem) {
        if let index = todos.firstIndex(where: { $0.id == todo.id }) {
            todos[index].isCompleted.toggle()
        }
    }
    
    private func deleteTodo(at offsets: IndexSet) {
        todos.remove(atOffsets: offsets)
    }
}
```

## Refinement Prompts

### Add Feature
```
Add the following feature to the existing app:
{feature_description}

Current implementation:
{current_code}

Maintain existing functionality while adding the new feature.
```

### Fix Issue
```
The following code has an issue:
{issue_description}

Current code:
{code_with_issue}

Fix the issue while maintaining the overall structure and functionality.
```

### Optimize Performance
```
Optimize the following code for better performance:
{code_to_optimize}

Focus on:
- Reducing unnecessary re-renders
- Improving algorithm efficiency
- Minimizing memory usage
```

## Validation Prompts

### Code Review
```
Review the following Swift code for:
1. Correctness and functionality
2. Swift best practices
3. Potential bugs or issues
4. Performance concerns
5. Code style and readability

Code:
{code_to_review}
```

### Test Generation
```
Generate unit tests for the following Swift code:
{code_to_test}

Include tests for:
- Happy path scenarios
- Edge cases
- Error conditions
- Boundary values
```
