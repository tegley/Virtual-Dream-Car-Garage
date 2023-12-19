#Import statements

#I used NumPy to import the csv file that contained all of my vehicle data and convert it to an array
import numpy as np

#Utilize Matplotlib's plotting and image processing capabilities
from matplotlib import pyplot as plt
from matplotlib import image as im

#I implemented the time module to add pauses throughout the program, thereby giving the user time to read on-screen messages
import time

import os #Suppress the Pygame welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

#The Pygame module is used to play the audio clip of the user's selected vehicle
from pygame import mixer
from pygame import time as tm

#The main function coordinates the execution of the entire program
def main():
    print("\033[31mWelcome To Timmy's Virtual Dream Car Garage \u00A9! \033[0m\n")
    time.sleep(2) #Add a pause so the user can read the welcome message
    data = np.loadtxt("Virtual_Dream_Car_Garage.csv",delimiter=",",dtype=str) #Import csv file
    dimensions = np.shape(data)
    total_rows = dimensions[0]
    Print_Brands(data,total_rows) #Print all available vehicle brands to the screen
    available_brands =  data[:,0] #The brands the user can choose from is stored in the 1st column of the array
    selected_brand = Get_Brand(available_brands) #Ask the user to choose a brand and check whether the brand they selected is valid              
    brand_row = Row_Finder(selected_brand, data, 1, total_rows, 0) #Determine the row of the user's selected vehicle brand
    final_vehicle_row = Print_Vehicles(data, brand_row) #Print all vehicles from the user's selected brand to the screen and determine the row of the final vehicle from that brand
    all_vehicles = data[:,1] #All vehicle choices are stored in the 2nd column of the array
    available_vehicles = data[brand_row:final_vehicle_row, 1] #The vehicles the user can choose from - row ranges from the row of the selected brand to the row of the final available vehicle choice
    selected_vehicle = Get_Vehicle(available_vehicles, all_vehicles) #Ask user to choose a vehicle and check whether the vehicle they selected is valid
    if selected_vehicle == 0: #Handle recursive case
        main()
    else: 
        car_data_row = Row_Finder(selected_vehicle, data, brand_row, final_vehicle_row, 1) #Determine the row in the csv file where image and audio data is stored
        year = data[car_data_row,2] #Determine the year of the user's selected vehicle
        image = "Image_Files/" + data[car_data_row,3] #Collect image file handle
        audio = "Audio_Files/" + data[car_data_row,4] #Collect audio file handle
        #Account for the fact that in the United States, luxury vehicles from Toyota are branded as Lexus and luxury vehicles from Honda are branded as Acura
        if selected_brand == 'Toyota' and selected_vehicle == 'LFA':
            selected_brand = 'Lexus'
        if selected_brand == 'Honda' and selected_vehicle == 'NSX (1st Gen)' or selected_vehicle == 'RSX' or selected_vehicle == 'NSX (2nd Gen)':
            selected_brand = 'Acura'
        Show_Image(image, year, selected_brand, selected_vehicle)
        Play_Audio(audio)
        print("\033[31mThank you for visiting Timmy's Virtual Dream Car Garage \u00A9! \033[0m") #Thank the user for using the program

#This function prints all available brands to the user
def Print_Brands(data, rows):
        print("AVAILABLE BRANDS")
        for i in range(1,rows): #Print all brands stored in the 1st column of the csv file
             if data[i,0] == '------------': #Break the loop when the end of the csv file is reached
                 break
             elif data[i,0] =="" or data[i,0] == 'Purdue':  #Don't print blank spaces and keep the Purdue brand hidden from the user
                  continue
             else:
                  print(data[i,0]) #Else, print the available brand (column 1 of the csv file)

#This function collects user input for brand choice
def Get_Brand(available_brands):
    valid = 0
    while valid == 0: #Continue asking the user to pick a brand until a valid choice has been made
        choice = input('\nSelect a brand - > ')
        if choice in available_brands: #If user input is valid, return their choice
            valid = 1
            return choice
        else: #Input validation
            print("Unfortunately, the brand you have selected is not featured in the collection. Please select a different brand.")    

#This function prints all available vehicle choices to the user
def Print_Vehicles(data, brand_row):
    print("\nAVAILABLE VEHICLES")
    while data[brand_row,1] != "": #Print all available vehicles from the selected brand
        print(data[brand_row,1])
        brand_row += 1
        if data[brand_row,1] == '------------': #Break the loop if the end of the csv file is reached (only applies when the user selects the last automotive brand)
            break        
    return brand_row #This is the row of the final available vehicle choice

#This function collects user input for their vehicle choice
def Get_Vehicle(available_vehicles, all_vehicles):
    #Lists of various incorrect vehicle choices - used for input validation
    SUVs = ['Urus','G Wagon','Cayenne','Purosangue','Macan','Mustang Mach-E','Durango SRT Hellcat','XM']
    Sedans = ['Camry','Civic','Accord','Malibu','Cruze','Fusion']
    Trucks = ['Silverado','Colorado','F150','Ridgeline','Frontier','Tacoma','Tundra']
    Minivans = ['Sienna','Odyssey','Pacifica']
    valid = 0
    while valid == 0: #Ask user to pick a car until a valid vehicle is selected
        choice = input('\nPick your car -> ')
        if choice in available_vehicles: #If user input is valid, return their choice
            valid = 1  
            return choice
        elif choice in all_vehicles: #If the user picks a vehicle that is available from a different brand within the collection, allow the user to re-select their brand
            print("It looks like the car you selected is from a different brand.")
            selection = input('Do you want to select that brand (y or n)? ')
            if selection=='y': #Re-execute the main function if the user agreees, thereby restarting the program
                choice = 0
                valid = 1
                return choice
            else:
                print("Then please pick a car from this brand.")
                valid=0
        elif choice not in all_vehicles: #Input validation
            if choice in SUVs: #Make fun of the user if they pick an SUV
                print("This isn't a dealership for rich soccer moms!")
                time.sleep(2)
                valid = 0
            elif choice in Sedans: #Make fun of the user if they pick a sedan
                 print("Boooring. You need to have bigger dreams than that!")
                 time.sleep(2)
            elif choice in Trucks: #Make fun of the user if they pick a truck
                 print("This is a dream CAR garage!")
                 time.sleep(2)
            elif choice in Minivans: #Make fun of the user if they pick a minivan
                 print("I'm so sorry that you actually want to listen to one of those atrocities.")
                 time.sleep(2)
            else: #Otherwise, ask the user to pick a vehicle contained within the collection
                print("Unfortunately, the vehicle you selected is not part of our collection. Please select one of the vehicles we have.")
                time.sleep(2)

#This function determines the row of the csv file that contains the user's valid input - it is called twice throughout the duration of the program
def Row_Finder(choice, data, start, end, column): #Determine the row of the user's input
    for row in range(start,end): #Check rows from the specified starting row to ending row
          if data[row,column] == choice: #When the user's input is found within the csv file, break the loop
                break
    return row #Return the row number of which the user's input was found

#This function displays the image of the user's selected vehicle
def Show_Image(image, year, selected_brand, selected_vehicle):
    display = im.imread(image)
    plt.imshow(display) #Display image
    plt.title(f"'{year} {selected_brand} {selected_vehicle}") #Display the make, model, and year of the user's selected vehicle
    plt.grid(False) #Format image
    plt.axis('off')
    plt.show()

#This function plays the exhaust note of the user's selected vehicle
def Play_Audio(audio):
    mixer.init() #Initiate the Pygame mixer
    mixer.music.load(audio) #Load and play the audio file
    mixer.music.play()
    while mixer.music.get_busy(): #Enusre that the entire audio file is played
        tm.Clock().tick(10)

if __name__ == '__main__': #Call the main function when the code is run (thereby running the entire program)
    main()