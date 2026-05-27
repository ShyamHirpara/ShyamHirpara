import urllib.request
import json
import re

def main():
    url = "https://api.github.com/users/ShyamHirpara/events/public"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print("Error fetching data:", e)
        return

    events_list = []
    for event in data:
        repo_name = event['repo']['name']
        repo_url = f"https://github.com/{repo_name}"
        event_type = event['type']
        
        # Skip events in the ShyamHirpara/ShyamHirpara repo to avoid cluttering with profile updates
        if repo_name == "ShyamHirpara/ShyamHirpara":
            continue
            
        if event_type == 'PushEvent':
            events_list.append(f"🚀 Pushed to [{repo_name}]({repo_url})")
        elif event_type == 'WatchEvent':
            events_list.append(f"🌟 Starred [{repo_name}]({repo_url})")
        elif event_type == 'CreateEvent':
            events_list.append(f"🎉 Created repository [{repo_name}]({repo_url})")
        elif event_type == 'IssuesEvent' and event['payload']['action'] == 'opened':
            events_list.append(f"🐛 Opened issue in [{repo_name}]({repo_url})")
        elif event_type == 'PullRequestEvent' and event['payload']['action'] == 'opened':
            events_list.append(f"🔥 Opened PR in [{repo_name}]({repo_url})")
        
        if len(events_list) >= 5:
            break

    if not events_list:
        events_list.append("No recent public activity outside of profile updates.")

    activity_text = "\n".join([f"{i+1}. {text}" for i, text in enumerate(events_list)])
    
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    # Replace content between <!-- activity:START --> and <!-- activity:END -->
    pattern = r'(<!-- activity:START -->\n)(.*?)(\n<!-- activity:END -->)'
    replacement = r'\g<1>' + activity_text + r'\g<3>'
    new_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    main()
