 # -*- coding: utf-8 -*-
print "Loading Modules Please wait..."
from datetime import datetime
from time import gmtime, strftime, localtime
start_time = datetime.now()


import os
import sys
import googlemaps 
import gmplot
import random
import csv
import pandas as pd
import time
import glob

text_file = open("addresses.txt", "r")
addresses = text_file.read().split('|')
check_address = (os.stat("addresses.txt").st_size == 0)
text_file.close()

text_file1 = open("places.txt", "r")
Search_words = text_file1.read().split('|')
check_places = (os.stat("places.txt").st_size == 0)
text_file1.close()

text_file2 = open("markers/api.txt", "r")
apis = text_file2.read().split('|')
len_apis = len(apis)
random_api = random.choice(apis)
print "Total no of available apis = " + str(len_apis)
text_file2.close()


#Looking for addresses and places to plot from text file 


bazooka = 1

while bazooka == 1 :

  if check_address == False and check_places == False : 
    bazooka = 0
    print "Going to look around for places and plot them with respect to addresses"
    stupid_loop = 1
    while stupid_loop == 1 : 
      try :
        stupid_loop = 0
        vc = int((raw_input("Please enter radius to look around in Km (either 12 or 24 for this project) :")))   #Radius to search within in meters
        while vc >500 or vc<=0 :
         print "Invalid Input"
         vc = int((raw_input("Please enter radius to look around in Km (either 12 or 24 for this project) :")))

        radi = vc * 1000
        print "Radius to look around = " + str(radi) + " meters"
      except :
        print "Invalid Input"
        stupid_loop = 1

    for address in addresses :
      address = address.strip()
      gmaps = googlemaps.Client(key=random_api)


      # Geocoding an address
      #address = "bimtech gr noida"
      geocode_result = gmaps.geocode(address)

      if len(geocode_result) != 0 : 

        # Getting lat lang and formatted address from random address
        lat = geocode_result[0]["geometry"]["location"]["lat"]
        lng = geocode_result[0]["geometry"]["location"]["lng"]
        formatted_address = geocode_result[0]["formatted_address"] 
        print lat
        print lng
        print formatted_address  
  # # Extracting place image
  #       place_id0 = geocode_result[0]['place_id']
  #       place_detail0 = gmaps.place(place_id0)
  #       try :
  #         image_no = 1
  #         place_detail0 = place_detail0['result']['photos']
  #         for picture in place_detail0 :
  #           print "Extracting Image " + str(image_no)
  #           photo_reference = picture['photo_reference']
  #           photo_width = picture['width']
  #           photo_height = picture['height']
  #           print photo_reference
  #           output_photo = gmaps.places_photo(photo_reference= photo_reference, max_width= photo_width, max_height= photo_height)
  #           print output_photo

  #           a = open("output_images\\"  + formatted_address + '[Image '+ str(image_no) + ']' +  '.jpg', 'wb') 
  #           for chunk in output_photo :
  #             if chunk:
  #               a.write(chunk)
  #           a.close()
  #           image_no = image_no + 1

  #       except :
  #         pass
  # #image extraction done

        #home_location = []

        gmap = gmplot.GoogleMapPlotter(lat , lng, 12, apikey = random_api)
        try :

        	gmap.marker(lat , lng, color= '#FFFFFF', title= address + "," + " " + formatted_address)
        except :
        	pass
        #gmap.heatmap([lat], [lng], threshold=20, radius=35, gradient=None, opacity=0.9)
        if vc == 24 : 
          gmap.circle(lat, lng, 8046.72, color='#FF0000')
          gmap.circle(lat, lng, 16093.4, color='#FF0000')
          gmap.circle(lat, lng, 24140.2, color='#FF0000')
        elif vc == 12 :
          gmap.circle(lat, lng, 4023.36, color='#FF0000')
          gmap.circle(lat, lng, 8046.72, color='#FF0000')
          gmap.circle(lat, lng, 12070.1, color='#FF0000')
        else :
          pass           


        #Searching nearby address



        text_file1 = open("places.txt", "r")
        Search_words = text_file1.read().split('|')
        print len(Search_words)

        
        filename = 'real.csv'
        f = open(filename,"w")
        headers = "Driving Distance,Travel Time, Latitude,Longitude\n"
        f.write(headers)

        filename1 = 'dummy.csv'
        o1 = open('dummy.csv','wb')
        f1 = csv.writer(o1)
        f1.writerow(['Actual Address'])
        
        filename2 = 'dummy2.csv'
        o2 = open('dummy2.csv','wb')
        f2 = csv.writer(o2)
        f2.writerow(['Search Keyword'])  

        filename07 = 'place_name.csv'
        o7 = open('place_name.csv','wb')
        f7 = csv.writer(o7)
        f7.writerow(['Place_name'])

        o3 = open('ratings.csv','wb')
        f3 = csv.writer(o3)
        f3.writerow(['Google review rating out of 5'])

        o4 = open('phone_no.csv','wb')
        f4 = csv.writer(o4)
        f4.writerow(['Phone No'])

        o5 = open('website.csv','wb')
        f5 = csv.writer(o5)
        f5.writerow(['Website'])

        o6 = open('map_link.csv','wb')
        f6 = csv.writer(o6)
        f6.writerow(['Google Map link'])

        o11 = open('total_review.csv','wb')
        f11 = csv.writer(o11)
        f11.writerow(['No of Ratings'])

        for Search_word in Search_words :                #Searching keyword
          Search_word = Search_word.strip()
          if Search_word == 'hospital' or Search_word == 'hospitals' or Search_word == 'Hospital' or Search_word == 'Hospitals' :
            random_color = '#B22222'
          else :
            random_color = '#228B22'  
          #print verification
          place_near = gmaps.places_nearby(location=(lat, lng), radius=(radi), keyword=(Search_word))



          boo_check = True 
          try :
            for_next_page = place_near['next_page_token']
            print for_next_page
            next_length = len([for_next_page])
          except :
            for_next_page = []
            next_length = len(for_next_page)

          while boo_check or next_length == 1 :
            boo_check = False
            place_near = place_near['results']
          
            

            latitudes = []
            longitudes = []
            durations = []
            distances = []
            actual_address = []




            for abc in place_near :
              
              latitude = abc['geometry']['location']['lat']
              longitude = abc['geometry']['location']['lng']
              place_name = abc['name'].encode(sys.stdout.encoding, errors='replace')
              print place_name
              place_id = abc['place_id']
              place_detail = gmaps.place(place_id)



              try :
                website = place_detail['result']['website']
              except:
                website = 'Not available'
              print website
              f5.writerow([website])

              try :
                rating = place_detail['result']['rating']
              except:
                rating = 'Not available'   
              print rating
              f3.writerow([rating])

              try :
                phone_no = place_detail['result']['formatted_phone_number']
              except:
                phone_no = 'Not available'   
              print phone_no
              f4.writerow([phone_no])

              try :
                map_link = place_detail['result']['url']
              except:
                map_link = 'Not available'  
              print map_link
              f6.writerow([map_link])


              try : 
                total_review = str(len(place_detail['result']['reviews']))
              except :
                total_review = str(0)
              f11.writerow([total_review])



              #calculating Distance, time taken to travel and the destination address
              raw_distance = gmaps.distance_matrix((lat, lng), (latitude,longitude), mode=('driving'), avoid=('ferries'), units=('metric'))
              rows = raw_distance['rows'][0]

              duration = rows['elements'][0]['duration']['text']
              distance = rows['elements'][0]['distance']['text']
              
              chk_di = distance[-2:]
              if chk_di == " m" : 
                distance = (float(str(distance)[:-2]) /1000) * 0.621371
                distance = round(distance, 2)
                distance = str(distance) + " Miles"                

              else : 
                distance = float(str(distance)[:-2]) * 0.621371
                distance = round(distance, 2)
                distance = str(distance) + " Miles"

              print distance, duration
              try :

              	destination_address = (place_name +' ' + raw_distance['destination_addresses'][0]).encode(sys.stdout.encoding, errors='replace')
              except :
              	pass
              print destination_address

    # #Extracting Images for the place              
              
    #           place_detail0 = place_detail
    #           try :
    #             image_no = 1
    #             place_detail0 = place_detail0['result']['photos']
    #             for picture in place_detail0 :
    #               print "Extracting Image " + str(image_no)
    #               photo_reference = picture['photo_reference']
    #               photo_width = picture['width']
    #               photo_height = picture['height']
    #               print photo_reference
    #               output_photo = gmaps.places_photo(photo_reference= photo_reference, max_width= photo_width, max_height= photo_height)
    #               print output_photo

    #               a = open("output_images\\" + destination_address + '[Image '+ str(image_no) + ']' + '.jpg', 'wb') 
    #               for chunk in output_photo :
    #                 if chunk:
    #                   a.write(chunk)
    #               a.close()
    #               image_no = image_no + 1
    #           except :
    #             pass

    # #Image extration completed




              print latitude, longitude
              # actual_address.append(destination_address)
              durations.append(duration)
              distances.append(distance)
              latitudes.append(latitude)
              longitudes.append(longitude)
              #for drawing straight line from home address to destination
              pathlat = lat,latitude
              pathlng = lng,longitude
              #gmap.plot(pathlat,pathlng, random_color, edge_width=7)
              try :

              	gmap.marker(latitude , longitude, color=random_color, title= place_name + ", " +'Distance = ' + distance + " " +  'Travel time = ' + duration)
              except :
              	pass
              data1 = distance + "," + duration + "," + str(latitude) + "," + str(longitude) + "\n"  
              f.write(data1)
              f1.writerow([destination_address])
              f2.writerow([Search_word])
              f7.writerow([place_name])

            time.sleep(2)
            try:
              place_near = gmaps.places_nearby(location=(lat, lng), keyword=(Search_word), page_token = (for_next_page)) 
              print "try loop got executed"
              boo_check = True
              print 'Last iteration'
              #print place_near 
            except :
              pass
         
            
            try :
              for_next_page = place_near['next_page_token']
              print for_next_page
              next_length = len([for_next_page])
            except :
              for_next_page = []
              next_length = len(for_next_page)

            gmap.scatter(latitudes,longitudes, color=random_color, size=80, marker=False)
           
        gmap.draw('[' + str(vc) + ' Km' + '] ' + address + '.html')
        f.close()
        o1.close()
        o2.close()
        o7.close()
        o3.close()
        o4.close()
        o5.close()
        o6.close()
        o11.close()

        df7 = pd.read_csv("place_name.csv")
        df1 = pd.read_csv("real.csv")
        df2 = pd.read_csv("dummy.csv")
        df9 = pd.read_csv("ratings.csv")
        df10 = pd.read_csv("phone_no.csv")
        df11 = pd.read_csv("website.csv")
        df12 = pd.read_csv("map_link.csv")
        df13 = pd.read_csv("total_review.csv")

        merged = df1.join(df2)
        merged.to_csv( "xyabcqw.csv", index=False) #merged.to_csv( address + ".csv", index=False)
        os.remove("real.csv")
        os.remove("dummy.csv")  
        df3 = pd.read_csv("dummy2.csv")
        df4 = pd.read_csv("xyabcqw.csv")
        merged = df3.join(df4).join(df7).join(df9).join(df13).join(df10).join(df11).join(df12)
        merged.to_csv('[' + str(vc) + ' Km' + '] ' + address + ".csv", index=False)
        os.remove("place_name.csv")
        os.remove("dummy2.csv")
        os.remove("xyabcqw.csv")
        os.remove("ratings.csv")
        os.remove("phone_no.csv")
        os.remove("website.csv")
        os.remove("map_link.csv")
        os.remove("total_review.csv")


      else : 
        print "Address can't be found please correct the address in text file"
        pass

  elif check_address and check_places :
    bazooka = 1
    print "Both addresses and places text file are empty, please provide values to any of them "

  elif not check_address and check_places :




    bazooka = 0


    all_files = glob.glob("addresses*")
    gmaps = googlemaps.Client(key=random_api)
    gmap = gmplot.GoogleMapPlotter(28.5577921 , 77.156244, 2, apikey = random_api)
    latitudes = []
    longitudes = []

    for file in all_files :
      name_file = file.replace("addresses_","").replace(".txt","")
      if len(name_file) > 2 :
        print "Going to plot only addresses on the map"
        addresses = open(file,"r").read().split("|")


        for address in addresses :

          geocode_result = gmaps.geocode(address)
          # Getting lat lang and formatted address from random address

          try :
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]
            formatted_address = geocode_result[0]["formatted_address"] 
            print lat
            print lng
            print formatted_address
            
            gmap.marker(lat , lng, color=  "#" + name_file, title= str(formatted_address))
            latitudes.append(lat)
            longitudes.append(lng)
            if name_file == "main":
                  gmap.circle(lat, lng, 40233.6, color='#FF0000')
                  gmap.circle(lat, lng, 80467.2, color='#FF0000')
                  gmap.circle(lat, lng, 160934, color='#FF0000')
          except :
            print "Address not found please enter a correct address"
    gmap.scatter(latitudes,longitudes, color='#1E90FF', size=80, marker=False)
    gmap.draw('Consolidated_address_plot.html')

  elif check_address and not check_places :
    bazooka = 1
    print "Address text file can't be left blank"
print "Execution completed successfully,you can close terminal...see ya next time :)"

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))












