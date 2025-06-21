# Final Project - Signal Visualization Application

## Overview
For your final project, you will create a PyQt application for real-time visualization of 32-channel signal data. The application will be structured using the Model-View-ViewModel (MVVM) architecture pattern, which separates the user interface from the business logic and data management. The application will receive data via TCP connection.

## Team Information
- This project will be completed in teams of 2 students
- Each team member should contribute equally to the project
- Clear division of responsibilities is recommended (e.g., one focusing on TCP/backend, one on visualization/frontend)

## Support and Contact
If you have any questions or need assistance during the project, you can:
- Visit us during the exercise sessions
- Contact us via email:
  - Daniel Fenzel: daniel.fenzel@fau.de
  - Raul Simpetru: raul.simpetru@fau.de

## Deadline
The final version of your project must be completed by:
- Sunday, 13.07.2024, 24:00
- We will fork the final version at this time

## Project Structure (just an example can be different)
```
final_project/
├── main.py                 # Application entry point
├── view/                   # View Layer
│   ├── mainView.py        # Main window implementation
│   └── otherView.py       # Custom visualization widgets
├── viewmodel/             # ViewModel Layer
│   ├── mainViewModel.py   # Business logic and state management
│   └── otherViewModel.py  # Business logic and state management
├── service/               # Service Layer
│   ├── dataProcess.py     # Data management and processing
│   └── tcpService.py      # TCP communication handling
```

### Application Features
Your application must include:

1. TCP Communication (Service Layer)
   - TCP connection management
   - Data stream reception
   - Handle data chunks of 32 channels × 18 samples
   - Data format: Each chunk contains:
     - 32 channels of data
     - 18 samples per channel
     - Total chunk size: 32 × 18 = 576 values

2. Real-time Signal Visualization (View Layer)
   - Live plotting of incoming TCP data using VisPy
   - Support for 32 channels
   - Channel selection mechanism
   - Single channel visualization at a time
   - Smooth real-time updates

3. Offline Signal Analysis after Transmission stopped (View Layer)
   - Complete signal visualization using Matplotlib
   - Ability to view the entire recorded signal
   - Channel selection for offline viewing
   - Basic signal analysis tools
     
#### Optional Feature Ideads
  - Change from unfiltered signal to filtered signal or RMS signal
  - STOP and RESUME Button
    

5. User Interface (View Layer)
   - TCP connection controls
   - Channel selection mechanism
   - Connection status display

## Requirements

### Technical Requirements
1. The application must be built using PyQt5
2. Strictly follow the MVVM architecture pattern:
   - Clear separation of concerns
   - All interactions through ViewModel
3. Use VisPy for real-time signal visualization
4. Use Matplotlib or VisPy for offline signal visualization
5. Handle 32-channel data streaming via TCP:
   - Implement TCP server/client functionality
   - Handle connection management
   - Process incoming data streams
   - Buffer management for smooth visualization
6. Handle errors appropriately:
   - Connection errors
   - Data parsing errors
   - Visualization errors

### Documentation
Include:
1. A detailed README.md explaining:
   - How to run the application
   - TCP connection specifications
   - Data format specifications
   - MVVM architecture implementation

2. Code documentation (docstrings and comments)

## Submission Requirements
1. Complete source code
2. README.md with setup and usage instructions
3. Requirements.txt file listing all dependencies
4. A brief presentation (5-10 minutes) explaining your application

## Grading Criteria
- MVVM Architecture Implementation
- TCP Communication and Data Handling
- Real-time visualization performance
- User interface and experience
- Documentation and presentation

## Tips
- Start with a clear plan and design
- Maintain strict MVVM separation
- Test TCP communication early
- Handle possible TCP connection scenarios
- Keep your code organized and well-documented
- Use version control (Git) to track your progress

Good luck with your final project! 
## Grading Criteria
- MVVM Architecture Implementation
- TCP Communication and Data Handling
- Real-time visualization performance
- User interface and experience
- Documentation and presentation

## Tips
- Start with a clear plan and design
- Maintain strict MVVM separation
- Test TCP communication early
- Handle possible TCP connection scenarios
- Keep your code organized and well-documented
- Use version control (Git) to track your progress

Good luck with your final project! 
