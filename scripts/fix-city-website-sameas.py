import os, glob

root = "/home/amram/WEBSITE"
sameas = '''  "sameAs": [
    "https://www.yelp.com/biz/amy-electric-los-angeles",
    "https://www.facebook.com/people/Amy-Electric/100063766463600/"
  ],'''

for path in glob.glob(os.path.join(root, "city-*.html")):
    with open(path) as f:
        content = f.read()

    old = '"url": "https://amyelectric.com",\n  "potentialAction"'
    new = f'"url": "https://amyelectric.com",\n{sameas}\n  "potentialAction"'

    if old in content:
        content = content.replace(old, new, 1)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Fixed: {os.path.basename(path)}")
    elif '"sameAs"' in content:
        print(f"Already has sameAs: {os.path.basename(path)}")
    else:
        print(f"Pattern not found: {os.path.basename(path)}")
        # Debug
        import re
        m = re.search(r'"url":\s*"https://amyelectric.com",', content)
        if m:
            print(f"  Found url line, next 80 chars: {repr(content[m.end():m.end()+80])}")
