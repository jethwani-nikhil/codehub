from bs4  import BeautifulSoup
import pywhatkit
import requests
import time
from datetime import datetime, timedelta
import json

# Initialize variables for previous notification
previous_notification = ""

while True:
    try:
        # Send an HTTP GET request to the URL and retrieve the page content
        html_text = requests.get('https://www.subodhpgcollege.com/notice_board').text

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_text, 'lxml')

        # Find all <ul> elements with class "list_none comment_list"
        news = soup.find(class_='tab-pane fade show active')
        lists = news.find('li', 'comment_info')
        content_element = lists.find(class_='comment_content')
        link_element = lists.find(class_='d-sm-flex align-items-center')

        # Check if the content element exists and extract the content
        content = content_element.text if content_element else "No content available"

        # Try to extract the link, if available
        linktopdf = link_element.h6.a['href'] if link_element and link_element.h6.a else ""

        # Construct the message
        if linktopdf:
            message = f"{content}\nwww.subodhpgcollege.com/{linktopdf}"
        else:
            message = content

        # Check if the current notification is different from the previous one
        if content != previous_notification:
            # Update the previous notification
            previous_notification = content

            # Calculate the time to send the notification (current time + 1 minute)
            send_time = datetime.now() + timedelta(minutes=1)
            send_hour = send_time.hour
            send_minute = send_time.minute

            # Send the WhatsApp message at the calculated time
            pywhatkit.sendwhatmsg_to_group('G8GzGghgzfG5wPdsge2Gbv', message, send_hour, send_minute)

            # Update the previous notification in the JSON file
            file_path = 'previous_content.json'
            with open(file_path, "w") as file:
                json.dump(previous_notification, file)

        # Print that no new news came and Sleep for 10 minutes before checking again
        print("No new news received.")
        time.sleep(600)

    except Exception as e:
        # Handle exceptions, e.g., network errors or issues with the website
        print(f"An error occurred: {str(e)}")
        time.sleep(600)  # Sleep for 10 minutes before retrying     