import requests
from bs4 import BeautifulSoup
import os
import re

# List of URL to scrape
urls = [
    "https://www.daniwinksflexibility.com/bendy-blog/build-a-better-hip-flexor-stretch",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-pnf-stretch-for-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/how-frequently-should-i-stretch",
    "https://www.daniwinksflexibility.com/bendy-blog/knee-friendly-hip-flexor-stretches",
    "https://www.daniwinksflexibility.com/bendy-blog/trouble-breathing-in-a-chest-stand-elevate-your-shoulders",
    "https://www.daniwinksflexibility.com/bendy-blog/cow-face-pose-arms-rear-hand-clasp",
    "https://www.daniwinksflexibility.com/bendy-blog/help-my-hips-hurt-in-frog-stretch-and-middle-split",
    "https://www.daniwinksflexibility.com/bendy-blog/why-and-how-to-warm-up-before-stretching",
    "https://www.daniwinksflexibility.com/bendy-blog/cold-vs-warm-flexibility-and-how-to-increase-cold-flexibility",
    "https://www.daniwinksflexibility.com/bendy-blog/help-my-back-hurts-after-backbending",
    "https://www.daniwinksflexibility.com/bendy-blog/is-it-ok-to-lift-the-heels-in-a-bridge-full-wheel",
    "https://www.daniwinksflexibility.com/bendy-blog/10-great-youtube-channels-for-flexibility-anatomy-education",
    "https://www.daniwinksflexibility.com/bendy-blog/my-top-5-insta-accounts-to-follow-for-flexibility-education",
    "https://www.daniwinksflexibility.com/bendy-blog/obturator-nerve-tension-test-amp-nerve-glide",
    "https://www.daniwinksflexibility.com/bendy-blog/passive-stretching-is-not-the-devil",
    "https://www.daniwinksflexibility.com/bendy-blog/lift-that-leg-7-stretches-for-a-higher-y-scale-leg-hold",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-do-a-y-scale-leg-hold",
    "https://www.daniwinksflexibility.com/bendy-blog/back-stretches-for-full-spinal-flexibility",
    "https://www.daniwinksflexibility.com/bendy-blog/i-can-open-my-hips-in-a-frog-stretch-but-not-middle-splits-what-gives",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-use-neck-engagement-for-a-deeper-cobra-pose",
    "https://www.daniwinksflexibility.com/bendy-blog/using-bands-to-help-support-square-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/building-visual-and-physical-awareness-for-square-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/what-to-do-on-your-rest-active-recovery-days",
    "https://www.daniwinksflexibility.com/bendy-blog/the-importance-of-rest-days-in-flexibility-training",
    "https://www.daniwinksflexibility.com/bendy-blog/struggling-to-keep-your-back-flat-in-a-forward-fold-5-tips-to-hinge-at-the-hips",
    "https://www.daniwinksflexibility.com/bendy-blog/is-it-ok-to-round-your-back-in-a-forward-fold",
    "https://www.daniwinksflexibility.com/bendy-blog/point-or-flex-protecting-your-ankles-in-middle-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/stop-leaning-forwards-in-your-front-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/proper-hip-alignment-for-middle-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/hip-anatomy-for-middle-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/example-chest-stand-training-progression",
    "https://www.daniwinksflexibility.com/bendy-blog/flat-split-on-the-floor-but-not-in-the-air-what-gives",
    "https://www.daniwinksflexibility.com/bendy-blog/proper-pelvis-position-for-hip-flexor-stretches",
    "https://www.daniwinksflexibility.com/bendy-blog/is-nerve-tension-limiting-your-shoulder-range-of-motion",
    "https://www.daniwinksflexibility.com/bendy-blog/easy-contortion-performance-makeup-for-people-who-are-crap-at-makeup",
    "https://www.daniwinksflexibility.com/bendy-blog/gentle-passive-stretches-for-internal-hip-rotation",
    "https://www.daniwinksflexibility.com/bendy-blog/6-active-flexibility-drills-for-internal-hip-rotation-mobility",
    "https://www.daniwinksflexibility.com/bendy-blog/my-contortion-warm-up-routine-an-example",
    "https://www.daniwinksflexibility.com/bendy-blog/help-my-outer-hips-hurt-when-i-straddle",
    "https://www.daniwinksflexibility.com/bendy-blog/shoulder-conditioning-for-contortion-forearm-stands",
    "https://www.daniwinksflexibility.com/bendy-blog/pincha-forearm-stand-tips-to-balance-like-an-instagram-yogi",
    "https://www.daniwinksflexibility.com/bendy-blog/3-ways-to-get-into-a-wall-supported-forearm-stand-pincha-pose",
    "https://www.daniwinksflexibility.com/bendy-blog/middle-split-oversplits-a-primer-on-technique",
    "https://www.daniwinksflexibility.com/bendy-blog/getting-a-pointier-toe-pointe",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-flatten-your-middle-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/4-foam-rolling-exercises-to-ease-a-sore-neck",
    "https://www.daniwinksflexibility.com/bendy-blog/7-oversplit-preparation-drills-for-active-front-split-flexibility",
    "https://www.daniwinksflexibility.com/bendy-blog/4-active-flexibility-drills-to-strengthen-your-front-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/am-i-too-old-to-start-contortion",
    "https://www.daniwinksflexibility.com/bendy-blog/controlling-rouge-hips-keeping-your-hips-square-in-a-split",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-tell-if-your-split-is-square-the-butt-cheek-test-and-more",
    "https://www.daniwinksflexibility.com/bendy-blog/why-your-upper-back-sucks-at-backbending-and-how-to-make-it-suck-less",
    "https://www.daniwinksflexibility.com/bendy-blog/what-muscles-do-i-need-to-stretch-for-the-front-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/work-your-active-split-flexibility-with-front-split-slides",
    "https://www.daniwinksflexibility.com/bendy-blog/advanced-quad-and-hip-flexor-stretches-for-contortion",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-femoral-nerve-glide-for-tight-hips-2-ways",
    "https://www.daniwinksflexibility.com/bendy-blog/stubbornly-tight-hip-flexors-how-to-test-for-femoral-nerve-tension",
    "https://www.daniwinksflexibility.com/bendy-blog/help-my-knee-hurts-in-a-lunge",
    "https://www.daniwinksflexibility.com/bendy-blog/straddle-vs-middle-split-whats-the-difference",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-get-your-leg-higher-in-three-legged-downard-dog",
    "https://www.daniwinksflexibility.com/bendy-blog/wrist-warm-up-for-handstands",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-active-straddle-hover",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-get-more-open-shoulders-in-a-bridge",
    "https://www.daniwinksflexibility.com/bendy-blog/not-making-progress-stretching-x-reasons-why",
    "https://www.daniwinksflexibility.com/bendy-blog/10-minute-middle-split-and-straddle-routine",
    "https://www.daniwinksflexibility.com/bendy-blog/knee-pain-in-middle-splits-try-these-adjustments",
    "https://www.daniwinksflexibility.com/bendy-blog/30-day-toe-touch-flexibility-challenge",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-close-the-last-inches-on-your-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-fake-a-split-aka-illusion-split",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-stand-up-from-a-bridge",
    "https://www.daniwinksflexibility.com/bendy-blog/4-active-hamstring-stretches-for-beginners",
    "https://www.daniwinksflexibility.com/bendy-blog/help-my-front-knee-hurts-in-a-split",
    "https://www.daniwinksflexibility.com/bendy-blog/3-beginner-friendly-calf-stretches-for-tight-calves",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-sit-in-a-chair-sit-bridge",
    "https://www.daniwinksflexibility.com/bendy-blog/how-to-sciatic-nerve-glide-for-happier-hamstrings",
    "https://www.daniwinksflexibility.com/bendy-blog/when-and-how-to-start-working-on-oversplits",
    "https://www.daniwinksflexibility.com/bendy-blog/6-active-flexibility-drills-for-a-flatter-straddle-pancake",
    "https://www.daniwinksflexibility.com/bendy-blog/the-importance-of-external-shoulder-rotation-in-a-backbend",
    "https://www.daniwinksflexibility.com/bendy-blog/contract-relax-stretches-for-middle-splits",
    "https://www.daniwinksflexibility.com/bendy-blog/forearmstands-for-beginners"
]

# Name of the folder where the text files will be saved
folder_name = "daniwinks_articles"
os.makedirs(folder_name, exist_ok=True)  # Create the folder if it doesn't exist

# Loop through all URLs
for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the blog title (assumes it's in an <h1> tag)
        title_tag = soup.find('h1')
        if title_tag:
            title = title_tag.text.strip()
        else:
            title = "no-title"

        # Use a regex to create a valid filename from the title (alphanumeric and hyphens only)
        filename = re.sub(r'[^a-zA-Z0-9\- ]', '', title).lower().replace(' ', '-')
        filepath = os.path.join(folder_name, f"{filename}.txt")
        
        # Extract the blog content (assumes it's inside the <div> with class 'sqs-block-content')
        content_divs = soup.find_all('div', class_='sqs-block-content')
        content = "\n\n".join(div.get_text(strip=True) for div in content_divs if div.get_text(strip=True))
        
        # Save the content to a text file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n{content}")
        print(f"Saved: {filepath}")
    else:
        print(f"Failed to retrieve: {url}")
        
