from selenium import webdriver
import requests
import re
import traceback

def get_user_agent(domain):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    driver.get(domain)
    user_agent = driver.execute_script("return navigator.userAgent;")
    print("User-Agent:", user_agent)
    driver.quit()
    return user_agent
    

def get_disallowed_paths(domain, user_agent):
    # Step 1: Fetch robots.txt
    robots_url = f"{domain}/robots.txt"
    response = requests.get(robots_url)
    
    # Check if the response was successful
    if response.status_code != 200:
        print(f"Failed to retrieve robots.txt: Status code {response.status_code}")
        return []

    robots_txt = response.text
    
    # Step 2: Parse robots.txt for the given User-Agent
    disallowed_paths = []
    is_matching_user_agent = False
    
    # Split robots.txt by lines
    lines = robots_txt.splitlines()
    
    for line in lines:
        # Remove any comments and leading/trailing whitespace
        line = line.split('#')[0].strip()
        
        # If line is empty, skip it
        if not line:
            continue
        
        # Check if this line defines a User-Agent
        if line.lower().startswith("user-agent"):
            # Extract the User-Agent name
            agent = line.split(":")[1].strip()
            # Check if this User-Agent matches the given one
            is_matching_user_agent = (agent == "*" or agent.lower() == user_agent.lower())
        
        # If we're in the correct User-Agent block, capture Disallowed paths
        elif is_matching_user_agent and line.lower().startswith("disallow"):
            # Extract the Disallowed path
            path = line.split(":")[1].strip()
            # Add to the list of disallowed paths if not empty
            if path:
                disallowed_paths.append(path)
    
    return disallowed_paths

def get_disallowed_list(domain_list):
    disallowed_path_list = []
    for domain in domain_list:
        try:
            user_agent = get_user_agent(domain=domain)
            disallowed_paths = get_disallowed_paths(domain, user_agent)
            
            for path in disallowed_paths:
                disallowed_path_list.append(f'{domain}{path}')
        except:
            print(traceback.format_exc())
    return disallowed_path_list


# # 예시 사용
# domain = "https://edition.cnn.com"
# user_agent = get_user_agent(domain=domain)
# disallowed_paths = get_disallowed_paths(domain, user_agent)

# print(f"Disallowed paths for '{user_agent}':")
# for path in disallowed_paths:
#     print(path)
