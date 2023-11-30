## Description

## Installation
1. Third-party installation / downloads
    1. Install Chrome Web Browser
        - https://www.google.com/chrome/
        - Go to ```Settings > About Chrome``` and take note of the browser version
    2. Download Chrome Driver
        - https://chromedriver.chromium.org/downloads
        - *Note, you'll need to download version compatable with Chrome Web Browser version
    3. Install Java JRE
        - https://www.java.com/en/
    4. Download Selenium Driver 4.1.0 Jar file
        - https://github.com/SeleniumHQ/selenium/releases/download/selenium-4.1.0/selenium-server-4.1.0.jar
        - You can find the link above by visiting https://www.selenium.dev/downloads/, and scrolling down and clicking on "Previous Releases"

    5. Install Python 3.7
        - https://www.python.org/downloads/
</br>

2. Clone repo
8. Open terminal, navigate to repo project root.

9. Setup virtual environment, in terminal enter:
    1. ```python3 -m venv venv``` - creates virtual environment 
    2. ```source venv/bin/activate``` - initializes virtual environment
       - ** Note - you should see ```(venv)``` in terminal when successful
10. Install project requirements to virtual envirnment
    - ```pip install -r requirements.txt```
  
11. Initialize Selenium Server
    - Make sure you have both downloads from step ```1.ii``` and ```1.iv``` in the same directory (does not have to be project directory)
    -  In terminal, navigate to that directory
    -  Run, ```java -jar selenium-server-4.1.0.jar standalone -p 4444```
        - This initiates selenium server on port 4444
   
  
## Sample - Command-line Pytest Invocation
-```CONFIG_PATH={path_to_project}/econ_calendar_automation/configs/local_config.json python3 -m "pytest" -s -v --disable-warnings "investing/tests/test_economic_calendar.py" ```
  - make sure to replace ```{path_to_project}``` with actual project path
    
