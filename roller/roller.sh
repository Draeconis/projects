#!/bin/bash

# interactive bash script to demo a few things;
# basic single-use dice roller
# dice roller with a loop to continue if required
# dice roller based on the Earthdawn system (goes beyond 30, but I'm not gonna do 100 for a POC!)

echo "What system are you using?"
echo "0: single dice roll"
echo "1: multiple dice rolls"
echo "2: Earth Dawn system"

read system

# basic single dice roll system with rudimentary validation that the input is an integer

if [[ "$system" == "0" ]]; then
  echo "Roll a dice of what size?"
  read size
  if [[ $size =~ ^-?[0-9]+$ ]]; then
    dice=`echo $[RANDOM%$size+1]`
    echo "Result is $dice"
    exit 0
  else
    echo "Input not an integer"
    exit 1
  fi
fi

# basic system for repeating dice rolls interactivly

if [[ "$system" == "1" ]]; then
  function diceroll {
    echo "Roll a dice of what size?"
    read size
    if [[ $size =~ ^-?[0-9]+$ ]]; then
      dice=`echo $[RANDOM%$size+1]`
      echo "Result is $dice"
    else
      echo "Input not an integer"
    fi
  }
  diceroll
  echo "New roll (y/n)?"
  read repeat
  while [[ "$repeat" == "y" ]]; do
    diceroll
    echo "New roll (y/n)?"
    read repeat
  done
  if [[ "$repeat" == "n" ]]; then
    exit 0
  fi
fi

# system to automate dice rolls using the earthdawn system, which ahs a concept of 'steps' and 'explosions'.
# a 'step' is a combination of different dice used in one roll.
# an 'explosion' is where a critical roll is achieved, and the same dice is rolled again, until the roll is not critical. the values of all rolls are added together.

if [[ "$system" == "2" ]]; then
  # http://arkanabar.tripod.com/steps.html used as a reference

  result=0
  internal_result=0

  IFS=","

  array[1]='4'
  array[2]='4'
  array[3]='4'
  array[4]='6'
  array[5]='8'
  array[6]='10'
  array[7]='12'
  array[8]='6,6'
  array[9]='8,6'
  array[10]='10,6'
  array[11]='10,8'
  array[12]='10,10'
  array[13]='12,10'
  array[14]='20,4'
  array[15]='20,6'
  array[16]='20,8'
  array[17]='20,10'
  array[18]='20,12'
  array[19]='20,6,6'
  array[20]='20,8,6'
  array[21]='20,10,6'
  array[22]='20,10,8'
  array[23]='20,10,10'
  array[24]='20,12,10'
  array[25]='20,10,8,4'
  array[26]='20,10,8,6'
  array[27]='20,10,8,8'
  array[28]='20,10,10,8'
  array[29]='20,12,10,8'
  array[30]='20,10,8,6,6'

  function roll() {
    roll=`echo $[RANDOM%$1+1]`
    echo "Roll from D$1 is $roll"
    let internal_result=internal_result+$roll
    while [[ "$roll" == "$1" ]]; do
      echo " -D$1 Crit!- "
      roll $1
    done
  }

  function step() {
    if [[ "$1" == "1" ]]; then
      roll 4
      let result=internal_result-2
    elif [[ "$1" == "2" ]]; then
      roll 4
      let result=internal_result-1
    elif [[ "$1" -gt "2" ]]; then
      for i in ${array[$1]}; do
        internal_result=0
        roll "$i"
        let result=result+internal_result
      done
    fi
  }

  echo "What step do you need to roll?"
  read step
  echo ""

  if [[ "$step" =~ ^-?[0-9]+$ ]]; then
    if (( $step <= "30" )); then
      step $step
      echo "-----"
      echo "Total is $result"
    else
      echo "Script does not support specified step."
    fi
  else
    echo "Value is not an integer."
  fi
fi

if [[ "$system" -gt 2 ]]; then
  echo "Function not implemented."
fi

exit 0
