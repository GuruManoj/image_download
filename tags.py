import urllib.request


def find_tags(s):
  tags = []
  for i in range(100):
  	start = s.find('<div class="ZO5Spb">')
  	if start == -1:
  		break
  	start_obj = s.find('data-ident="',start) + 12
  	end_obj = s.find('"',start_obj)
  	tag = s[start_obj:end_obj]
  	tags.append(tag)
  	s = s[end_obj:]
  return tags




searchtext = "car"
searchtext = "+".join(searchtext.strip().split(" "))
url = "https://www.google.co.in/search?q="+searchtext+"&source=lnms&tbm=isch"

try:
 headers = {}
 headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
 req = urllib.request.Request(url, headers=headers)
 #print(1)
 resp = urllib.request.urlopen(req)
 respData = str(resp.read())
 tags = find_tags(respData)
 print(tags)
except Exception as e:
  print(str(e))



