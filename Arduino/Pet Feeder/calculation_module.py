from datetime import datetime
import time

def calculation(petName, petWeight, targetWeight, foodEaten, waterEaten):
  dietFactor = targetWeight/petWeight #returns correction factor in diet relative to target weight
  #if targetWeight < petWeight then dietFactor < 1 to indicate less food

  foodGoal = petWeight * dietFactor * 27  # daily food goal adjusted for dietary needs
  waterGoal = petWeight * 30  # water should be based on current weight not target
  
  consumptionProgress(foodEaten, waterDrank, foodGoal, waterGoal, petName)

  foodNeed = str(petName) + " needs " + str(foodGoal) + "g of food"
  waterNeed = str(petName) + " needs " + str(waterGoal) + "mL of food"

def dailyGoal(petWeight, targetWeight):
    # Constants for food and water calculation
    baseFoodIntakePerLb = 50 / 2.20462    # grams of food per pound of body weight
    baseWaterIntakePerLb = 80 / 2.20462   # mL of water per pound of body weight
    adjustmentFactor = 0.2                # Adjust food intake by 20%

    # Convert petWeight and targetWeight from string to float
    petWeight = float(petWeight)
    targetWeight = float(targetWeight)

    # Calculate base food intake based on current weight
    foodGoal = petWeight * baseFoodIntakePerLb

    # Calculate base water intake based on current weight
    waterGoal = petWeight * baseWaterIntakePerLb

    # Adjust food intake based on weight difference
    weightDifference = targetWeight - petWeight

    if weightDifference > 0:
        # Increase food intake if target weight is greater than current weight
        foodGoal *= (1 + adjustmentFactor)
    elif weightDifference < 0:
        # Decrease food intake if target weight is less than current weight
        foodGoal *= (1 - adjustmentFactor)

    return foodGoal, waterGoal

def consumptionProgress(foodEaten, waterDrank, foodGoal, waterGoal, petName):
  foodProgress = (foodEaten / foodGoal) * 100; #create percent of goal
  waterProgress = (waterDrank / waterGoal) * 100;

  foodString = str(petName) + " has eaten " + str(foodProgress) + "% of their daily food goal"
  waterString = str(petName) + " has drank " + str(waterProgress) + "% of their daily water goal"

  goalDict1 = { #creates a dictionary with the date: true/false format
    'Date MM/DD/YYYY': 'Goal met? (true/false)'
  } #this one is for food

  goalDict2 = { #creates a dictionary with the date: true/false format
    'Date MM/DD/YYYY': 'Goal met? (true/false)'
  } #this one is for water

  if foodProgress >= 100:
    foodGoalMet = current_date()
    goalDict1[foodGoalMet] = 'true' #adds todays date with value true
  else:
    foodGoalMet = current_date()
    goalDict1[foodGoalMet] = 'false' #adds todays date with value false

  if waterProgress >= 100:
    waterGoalMet = current_date()
    goalDict2[waterGoalMet] = 'true' #adds todays date with value true
  else:
    waterGoalMet = current_date()
    goalDict2[waterGoalMet] = 'false' #adds todays date with value false
    #does not allow duplicates so will update for todays date if one already exists
  
  return

def current_time():
  return datetime.now().strftime('%m-%d-%Y %H:%M:%S') #creates string with MM/DD/YYYY and HR:Min:sec

def current_date():
  return datetime.now().strftime('%m-%d-%Y') #creates string with MM/DD/YYYY
  
