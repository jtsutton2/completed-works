#include <Servo.h>
#include <HX711_ADC.h>
#if defined(ESP8266)|| defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif

/***************************/
//         MACROS          //
//*************************//

    #define TRUE 1
    #define FALSE 0
    #define RESET 0
    #define TIME_MSG_LEN 11
    #define TIME_HEADER 'T'

/***************************/
// Function Declarations //
//*************************//

    // Initialization functions
        void Init_Serial (void);                            // Initializing Serial Communications
        void Init_Load_Cells (void);                        // Initializing Load Cells
        void Init_Servo (void);                             // Initializing Servo Motors
        void Init_Buttons(void);                            // Initializing Buttons
        void setupLoadCells(void);                          // This function must be called in the setup phase of main file

    // Scale-related functions
        void readFoodScale(float &reading);                 // Reads the food scale
        void readWaterScale(float &reading);                // Reads the water scale
        void tareOperations (void);                         // Used to zero or null out the scale reading if nothing is on it
        void printScale (float value);                      // Prints the value that was just weighed (value)
        void resetReadings (void);                          // Used to reset ReadingA and ReadingB

    // Food-related functions
        void dispenseFood(void);                            // Runs the motors to dispense food
        void foodOperations(void);                          // This is the function called from main for all food-related operations
        bool didPetEat(float first, float second);          // Did the pet eat?
        void foodUpdate(float amountEaten);                 // Add to the total amount eaten
        void resetFoodEaten(void);                          // Reset FoodEaten value (probably after the day is over or something)

    // Water-related functions
        void waterOperations(void);                          // This is the function called from main for all food-related operations
        bool didPetDrink(float first, float second);         // Did the pet eat?
        void waterUpdate(float amountEaten);                 // Add to the total amount eaten
        void resetWaterDrank(void);                          // Reset FoodEaten value (probably after the day is over or something)

    // Button-related functions
        bool checkButton (void);                            // Check if the pushbutton is pressed

    // Cooldown-related functions
        unsigned long currentTime(void);                    // Returns current timestamp in seconds
        unsigned long cooldown (unsigned long delay);       // Returns current time + delay for use as a cooldown

    // Pet-related functions
        float howMuchToEat(float weight);                   // Used to calculate how much food in grams a pet should eat daily based on bodyweight in pounds
        float howMuchToDrink(float weight);                 // Used to calculate how much water in milliliters a pet should drink daily based on bodyweight in pounds
        float consumptionProgress(void);                    // Used to calculate what percentage of food and water goals were met


/***************************/
// Global Variables //
//*************************//
    // Pet-related variables
        float petWeight;
        float dailyFoodAmount, dailyWaterAmount;
        float foodProgress, waterProgress;

    // Food-related variables
        int WaterDrank, WaterReset;
        float foodEaten = 0;                                // Sum of all weight unloaded (food consumed) from food scale
        float waterDrank = 0;
        bool petAte = false;
        bool petDrank = false;

    // Button-related variables
        int ButtonState;                                    // For reading and storing the pushbutton status
        int dispenseCount;                                  // Counts number of times dispense happens

    // Cooldown-related variables
        unsigned long foodCooldown, foodEatenCooldown;
        unsigned long myCooldown;
        unsigned long consumptionCooldown;
        unsigned long readingCooldown;
        int cycleCount;
        bool isFirstReading = true;


    // Servo Objects and fields
        Servo myservo;
        int speed;

    // Pins:
        //Load Cells Pins
            const int HX711_dout_1 = 4;     //mcu > HX711 no 1 dout pin
            const int HX711_sck_1 = 5;      //mcu > HX711 no 1 sck pin
            const int HX711_dout_2 = 8;     //mcu > HX711 no 2 dout pin
            const int HX711_sck_2 = 9;      //mcu > HX711 no 2 sck pin
    
        // Josh's Load Cell Pins
            const int FoodPin = 9;          //analog GPIO pin 9
            const int WaterPin = 10;        //analog GPIO pin 10

        // Motor Pins
            const int directionPin = 12;    //Digital GPIO D6
            const int pwmPin = 3;           //AREF for PWM
            const int brakePin = 9;         //Digital GPIO D9

        //Button Pins
            const int buttonPin = 2;

        // Load Cell / EEPROM variables
            float foodReading, waterReading;
            float tempFood, tempWater;

            //HX711 constructor (dout pin, sck pin)
            HX711_ADC LoadCell_1(HX711_dout_1, HX711_sck_1);    //HX711 1
            HX711_ADC LoadCell_2(HX711_dout_2, HX711_sck_2);    //HX711 2
            const int calVal_eepromAdress_1 = 0;                // eeprom adress for calibration value load cell 1 (4 bytes)
            const int calVal_eepromAdress_2 = 4;                // eeprom adress for calibration value load cell 2 (4 bytes)
            unsigned long t = 0;

constexpr unsigned long printInterval{ 1000 };
unsigned long printNow{};

int ScalesReady = FALSE;
int ButtonReady = FALSE;
int UserPromptNeeded = TRUE;
String UserQuestion1 = "Is your pet a dog or cat?";
String UserQuestion2 = "How much (in pounds) does your pet weigh? Please round to the nearest whole number.";



//function defines
void ScaleValue(void);
void food(void);
void RunButton(void);
void WaterValue(void);