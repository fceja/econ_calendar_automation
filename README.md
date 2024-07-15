# Description
Uses Selenium Webdriver and Pytest to parse economic calendar data from [investing.com](https://www.investing.com/economic-calendar/). </br>
Also outputs the data into a csv.

## Installation
![](https://img.shields.io/badge/OS-Linux%20%7C%20MacOS%20%7C%20Windows-eaeaea)
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

6. Create virtual environment, at project root run:
    1. Linux / maxOS
        - ```
          python3 -m venv venv
          ```
    2. Windows
        - ```
          python -m venv venv
          ```
7. Initiate virtual environment, at project root run:
    1. Linux / maxOS
        - ```
          source venv/bin/activate
          ```
    2. Windows
        - ```
          ./bin/activate
          ```
    3. ** Note - you should see `(venv)` in terminal when successful
       
8. Install dependencies
    - ```
      pip install -r requirements.txt
      ```
  
9. Initialize Selenium Server
    - Make sure you have both downloads from step ```1.ii``` and ```1.iv``` in the same directory (does not have to be project directory)
    -  In terminal, navigate to that directory
    -  Run, ```java -jar selenium-server-4.1.0.jar standalone -p 4444```
        - This initiates selenium server on port 4444
   
10. Create a free account from investing.com
    - include the credentials in ```/configs/local_config.json```
        - In the json file, replace the empty strings:
            - testProperties['investingAccountEmail']               
            - testProperties['investingAccountPassword']               
  
## Sample - Command-line Pytest Invocation
1. Linux / maxOS
    - ```
      CONFIG_PATH={path_to_project}/econ_calendar_automation/configs/local_config.json python3 -m "pytest" -s -v --disable-warnings "investing/tests/test_economic_calendar.py"
      ```
3. Windows
    - ```
      CONFIG_PATH={path_to_project}/econ_calendar_automation/configs/local_config.json python -m "pytest" -s -v --disable-warnings "investing/tests/test_economic_calendar.py"
      ```
  - make sure to replace ```{path_to_project}``` with actual project path
  - you'll see a csv created after running test -> ```/output/{date}/output.csv```
  - dates are configurable on lines 34 and 35 in -> ```/investing/tests/test_economic_calender.py```
    
### Tools & Platforms
<p>
    <a href="https://www.python.org/" target="_blank" rel="noreferrer">
        <img
          src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg"
          alt="python"
          width="70"
          height="70"
        /></a>
    <a href="https://www.selenium.dev/documentation/webdriver/" target="_blank" rel="noreferrer">
        <img
          src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/selenium/selenium-original.svg"
          alt="selenium"
          width="70"
          height="70"
        /></a>
</p>
