"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_generated = 0.0     # Total cookies generated throughout the game
        self._current_cookies = 0.0             # Current number of cookies you have
        self._current_time = 0.0                # Current time in seconds
        self._cps = 1.0                         # Cookies per second
        self._history = [(0.0, None, 0.0, 0.0)] # A list of tuples where each entry in the tuple is:
                                                # - A time
                                                # - An item that was bought at that time (or None), 
                                                # - The cost of the item
                                                # - The total number of cookies produced by that time
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("Total cookies generated: " + str(self._total_cookies_generated) + "\n" +
               "Current cookies: " + str(self._current_cookies) + "\n" + 
               "Current time: " + str(self._current_time) + "\n" + 
               "CPS: " + str(self._cps) + "\n") 
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """        
        if cookies - self._current_cookies >= 0:
            return math.ceil((cookies - self._current_cookies) / self._cps)
        else:
            return 0.0
        
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """      
        if time > 0:
            self._current_time += time
            self._current_cookies += (time*self._cps)
            self._total_cookies_generated += (time*self._cps)          
        else:
            return 
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies >= cost:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies_generated))
            
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    # Create a clone for build info
    build_info_clone = build_info.clone()
    
    # Create a new ClickerState object
    clicker_state = ClickerState()
    
    # Iteration to control the simulation time
    while clicker_state.get_time() <= duration:
        # Determine the item to buy next
        item_to_buy = strategy(clicker_state.get_cookies(), clicker_state.get_cps(), duration - clicker_state.get_time() , build_info_clone)
        
        # Break the loop if the item is None
        if item_to_buy is None:
            break
        
        # Determine how much time must elapse until it is possible to purchase the item. 
        elapsed = clicker_state.time_until(build_info_clone.get_cost(item_to_buy))
        
        # If you would have to wait past the duration of the simulation to purchase the item, 
        # you should end the simulation.
        if clicker_state.get_time() + elapsed > duration:
            break
            
        # Wait until that time
        clicker_state.wait(elapsed)
        
        # Buy the item
        clicker_state.buy_item(item_to_buy, build_info_clone.get_cost(item_to_buy), build_info_clone.get_cps(item_to_buy))
        
        # Update build information
        build_info_clone.update_item(item_to_buy)        
    
    # If exited the loop, wait until the end of the simulation
    clicker_state.wait(duration - clicker_state.get_time())    
    
    return clicker_state

def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    This strategy buys always the cheapest item
    """
    # Get the items list
    item_list = build_info.build_items()
    
    # Get the minimal cost item in list and its cost
    minval = float("inf")
    minidx = None
    for idx in range(len(item_list)):
        if build_info.get_cost(item_list[idx]) < minval:
            minval = build_info.get_cost(item_list[idx])
            minidx = idx
    
    # Minimum cost item in format [item_name, cost]
    min_cost_item = (item_list[minidx], build_info.get_cost(item_list[minidx]))
    
    # Return the object if I can buy it or None to exit
    if min_cost_item[1] <= (time_left * cps + cookies):
        return min_cost_item[0]
    else:
        return None

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    This strategy buys always the most expensive item
    """
    # Get the items list
    item_strings = build_info.build_items()
    
    # Get the item and their costs 
    item_list = []
    for item in item_strings:
        item_list.append((build_info.get_cost(item), item))
    
    # Sort the list in reverse in terms of item cost
    item_list.sort(reverse=True)
    
    # Return the most expensive item for the time that's left   
    for item in item_list:
        if item[0] <= (time_left * cps + cookies):
            return item[1]      
    return None

def strategy_best(cookies, cps, time_left, build_info):
    """
    This strategy is the best possible to optimize the number
    of generated cookies.
    
    In this case I have chosen a random selector
    """
    # Get the items list
    item_strings = build_info.build_items()
    
    # Get the item and their costs 
    item_list = []
    for item in item_strings:
        item_list.append((build_info.get_cost(item), item))
    
    # Sort the list in reverse in terms of item cost
    item_list.sort(reverse=True)
    
    # Return a random element
    random_idx = random.choice(range(len(item_list)))
    while item_list[random_idx][0] <= (time_left * cps + cookies):
        random_idx = random.choice(range(len(item_list)))
        return item_list[random_idx][1]
    return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()