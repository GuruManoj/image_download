from selenium import webdriver
import urllib
import json
import urllib
import os
import time

os.environ["PATH"] += os.pathsep + os.getcwd()  #for  geckodrive

def open_browser():
  driver = webdriver.Firefox()
  return driver

def close_browser(driver):
  driver.quit()

def fetch_links(driver, searchtext="car", count_argv=10, download_path="./download", tags = None):
  num_requested = int(count_argv)
  number_of_scrolls = num_requested / 400 + 1
  if not tags:
    tag = ""
    tags = ""
  else:
    tag = tags
    tags = "&chips=q:%s,%s"%(searchtext,"+".join(tags.split(" ")))
  url = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch%s"%(searchtext,tags)
  #extensions = ["jpg", "jpeg", "png"]
  #img_count = 0
  #downloaded_img_count = 0
  driver.get(url)
  for _ in range(int(number_of_scrolls)):
    for _ in range(10):
      driver.execute_script("window.scrollBy(0, 1000000)")
      time.sleep(0.2)
    time.sleep(0.5)
    try:
      driver.find_element_by_xpath("//input[@value='Show more results']").click()
    except Exception as e:
      print ("Less images found:", e)
      break
  images = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
  print ("Total images:", len(images), "\n")
  return images


def download_img(driver, searchtext="car", count_argv=10, download_path="./download", tags = None,images = []):

  '''
  num_requested = int(count_argv)
  number_of_scrolls = num_requested / 400 + 1 
  '''
  
  if not tags:
    tag = ""
    tags = ""
  else:
    tag = tags
    tags = "&chips=q:%s,%s"%(searchtext,"+".join(tags.split(" ")))
  #url = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch%s"%(searchtext,tags)
  extensions = ["jpg", "jpeg", "png"]
  #img_count = 0
  #downloaded_img_count = 0
  '''
  driver.get(url)
  for _ in range(int(number_of_scrolls)):
    for _ in range(10):
      driver.execute_script("window.scrollBy(0, 1000000)")
      time.sleep(0.2)
    time.sleep(0.5)
    try:
      driver.find_element_by_xpath("//input[@value='Show more results']").click()
    except Exception as e:
      print ("Less images found:", e)
      break
  images = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
  print ("Total images:", len(images), "\n")
  '''
  headers = {}
  headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
  dict_img = {}
  searchtext = "_".join([searchtext , tag.split(":")[1]])
  if not os.path.exists(download_path + "/" + searchtext.replace(" ", "_")):
    os.makedirs(download_path + "/" + searchtext.replace(" ", "_"))
  count = 1
  for x, img in enumerate(images):
    img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
    img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
    try:
      if img_type in extensions:
        #urllib.urlretrieve(img_url , "%s/img%s%s"%(download_path,str(x),img_type))
        f = open(download_path+"/"+searchtext.replace(" ", "_")+"/"+searchtext.replace(" ", "_")+str(count)+"."+img_type, "wb")
        req = urllib.request.Request(img_url, headers=headers)
        timeout = 1
        raw_img = urllib.request.urlopen(req, timeout = 1).read()
        print("download count : %s \nurl : %s"%(count, img_url))
        f.write(raw_img)
        f.close
        dict_img["x"] = {"ou":img_url, "ity":img_type}
        count = count + 1
    except Exception as e:
      print ("Download failed:", e)
    if count_argv < count :
      break
  if count_argv > count:
    print ("Less number of images found please enter different search phrase or tag")
  print("total downloads : %s"%count)
  #url = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch%s"%("tags","")
  #driver.get(url)
driver = open_browser()
images = fetch_links(driver, searchtext="car", count_argv=100, download_path="./download", tags = 'g_9:rare')
download_img(driver, searchtext="car", count_argv=100, download_path="./download", tags = 'g_9:rare' ,images = images)
close_browser(driver)



