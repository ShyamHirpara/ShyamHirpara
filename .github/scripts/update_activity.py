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
    seen_events = set()
    
    for event in data:
        repo_name = event['repo']['name']
        repo_url = f"https://github.com/{repo_name}"
        event_type = event['type']
        
        # Skip automated bot commits to prevent spamming the activity feed
        if event_type == 'PushEvent':
            commits = event.get('payload', {}).get('commits', [])
            is_bot = False
            for c in commits:
                author_name = c.get('author', {}).get('name', '')
                message = c.get('message', '')
                if 'github-actions' in author_name or 'Update recent GitHub activity' in message or 'Generated 3D Profile Contrib' in message:
                    is_bot = True
                    break
            if is_bot:
                continue
            
        event_str = None
        if event_type == 'PushEvent':
            event_str = f"🚀 Pushed to [{repo_name}]({repo_url})"
        elif event_type == 'WatchEvent':
            event_str = f"🌟 Starred [{repo_name}]({repo_url})"
        elif event_type == 'CreateEvent':
            event_str = f"🎉 Created repository [{repo_name}]({repo_url})"
        elif event_type == 'IssuesEvent' and event['payload']['action'] == 'opened':
            event_str = f"🐛 Opened issue in [{repo_name}]({repo_url})"
        elif event_type == 'PullRequestEvent' and event['payload']['action'] == 'opened':
            event_str = f"🔥 Opened PR in [{repo_name}]({repo_url})"
        
        # Add to list if it's a valid tracked event and not a duplicate
        if event_str and event_str not in seen_events:
            events_list.append(event_str)
            seen_events.add(event_str)
            
        if len(events_list) >= 5:
            break

    if not events_list:
        events_list.append("No recent public activity.")

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
