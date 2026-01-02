# Example Prompts

This directory contains example prompts you can use with NaturalPromptXcode.

## Basic Examples

### Counter App
```bash
python naturalpromptxcode.py "Create a simple counter app with increment and decrement buttons"
```

**Description**: Generates a basic counter app with two buttons and a display label.

**Expected Features**:
- Counter state management
- Increment button
- Decrement button
- Real-time display update

---

### Todo List
```bash
python naturalpromptxcode.py "Build a todo list app where users can add, complete, and delete tasks"
```

**Description**: Creates a task management app with full CRUD operations.

**Expected Features**:
- Add new tasks
- Mark tasks as complete
- Delete tasks
- List view
- Text input field

---

### Weather Display
```bash
python naturalpromptxcode.py "Create a weather app that shows current temperature and conditions"
```

**Description**: Generates a weather information display app.

**Expected Features**:
- Temperature display
- Weather condition text
- Weather icon
- Clean, modern UI

---

## Intermediate Examples

### Note Taking App
```bash
python naturalpromptxcode.py "Create a note-taking app where users can create, edit, and delete notes with titles and content"
```

**Expected Features**:
- Note list view
- Create new notes
- Edit existing notes
- Delete notes
- Title and content fields
- Navigation between views

---

### Timer App
```bash
python naturalpromptxcode.py "Build a countdown timer app with start, pause, and reset buttons"
```

**Expected Features**:
- Time display
- Start/pause toggle
- Reset functionality
- Progress indicator
- Sound notification (optional)

---

### Calculator
```bash
python naturalpromptxcode.py "Create a basic calculator app with addition, subtraction, multiplication, and division"
```

**Expected Features**:
- Number pad
- Operation buttons
- Display area
- Clear function
- Basic arithmetic operations

---

## Advanced Examples

### Photo Gallery
```bash
python naturalpromptxcode.py "Create a photo gallery app that displays images in a grid layout with detail view"
```

**Expected Features**:
- Grid layout
- Image loading
- Detail view navigation
- Zoom capability
- Responsive design

---

### Settings Screen
```bash
python naturalpromptxcode.py "Build a settings screen with toggle switches for notifications, dark mode, and a slider for font size"
```

**Expected Features**:
- Toggle switches
- Slider controls
- Grouped settings
- Save preferences
- Standard settings UI

---

### Login Form
```bash
python naturalpromptxcode.py "Create a login screen with email and password fields, validation, and a login button"
```

**Expected Features**:
- Email text field
- Secure password field
- Input validation
- Login button
- Error messaging
- Keyboard handling

---

## Tips for Writing Good Prompts

### Be Specific
❌ "Make an app"
✅ "Create a counter app with increment and decrement buttons"

### Describe the UI
❌ "Build a todo app"
✅ "Build a todo list app with a text field to add tasks, a list to show tasks, and ability to mark tasks as complete"

### Mention Key Features
❌ "Create a weather app"
✅ "Create a weather app that shows temperature, weather condition text, and an icon representing the current weather"

### Specify Interactions
❌ "Make a photo app"
✅ "Create a photo gallery with a grid of images that can be tapped to view in full screen"

## Running Examples

### Basic Usage
```bash
python naturalpromptxcode.py "YOUR_PROMPT_HERE"
```

### With Options
```bash
python naturalpromptxcode.py "YOUR_PROMPT_HERE" \
  --output-dir ~/Projects/MyApp \
  --ui-framework swiftui \
  --verbose
```

### Dry Run (Generate Only)
```bash
python naturalpromptxcode.py "YOUR_PROMPT_HERE" --dry-run
```

## Experiment and Iterate

Feel free to modify these prompts or create your own! The system works best when you:
- Start simple and add complexity gradually
- Be specific about UI elements
- Mention user interactions clearly
- Describe the core functionality

Happy coding! 🚀
