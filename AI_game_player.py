import streamlit as st
import random
import time

st.set_page_config(page_title="AI Snake Player", page_icon="🐍")
st.title("🐍 AI Game Player: Self-Driving Snake")
st.write("Watch the automated AI agent play Snake by calculating the shortest path coordinates to the food target.")

# Initialize grid variables
GRID_SIZE = 15

if 'snake' not in st.session_state:
    st.session_state.snake = [(7, 7)]
    st.session_state.food = (3, 3)
    st.session_state.score = 0
    st.session_state.game_over = False

def reset_game():
    st.session_state.snake = [(7, 7)]
    st.session_state.food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    st.session_state.score = 0
    st.session_state.game_over = False

# AI Pathfinding Decision Engine
def get_ai_move(snake, food):
    head_x, head_y = snake[0]
    food_x, food_y = food
    
    # Try to move closer horizontally first, then vertically
    if head_x < food_x and (head_x + 1, head_y) not in snake:
        return (head_x + 1, head_y)
    elif head_x > food_x and (head_x - 1, head_y) not in snake:
        return (head_x - 1, head_y)
    elif head_y < food_y and (head_x, head_y + 1) not in snake:
        return (head_x, head_y + 1)
    elif head_y > food_y and (head_x, head_y - 1) not in snake:
        return (head_x, head_y - 1)
    
    # Emergency fallback check if optimal path is blocked
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        next_step = (head_x + dx, head_y + dy)
        if 0 <= next_step[0] < GRID_SIZE and 0 <= next_step[1] < GRID_SIZE and next_step not in snake:
            return next_step
    return None

# Control Buttons
col1, col2 = st.columns(2)
with col1:
    run_ai = st.checkbox("🤖 Activate AI Player Loop")
with col2:
    if st.button("🔄 Reset Field"):
        reset_game()

# Execution Step
if run_ai and not st.session_state.game_over:
    next_move = get_ai_move(st.session_state.snake, st.session_state.food)
    
    if next_move is None or not (0 <= next_move[0] < GRID_SIZE and 0 <= next_move[1] < GRID_SIZE):
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, next_move)
        if next_move == st.session_state.food:
            st.session_state.score += 1
            while True:
                new_food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                if new_food not in st.session_state.snake:
                    st.session_state.food = new_food
                    break
        else:
            st.session_state.snake.pop()
    time.sleep(0.2)
    st.rerun()

# Draw Game Field Interface
st.metric("Current Target Score", f"{st.session_state.score} Points")

if st.session_state.game_over:
    st.error("💥 Collision Detected! Game Over.")
else:
    # Render visual grid board
    grid_html = "<div style='display: grid; grid-template-columns: repeat(15, 25px); gap: 2px;'>"
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if (x, y) == st.session_state.snake[0]:
                color = "#00FF00" # Green for head
            elif (x, y) in st.session_state.snake:
                color = "#82E0AA" # Light green for tail
            elif (x, y) == st.session_state.food:
                color = "#FF4136" # Red for food
            else:
                color = "#2C3E50" # Dark gray empty background
            grid_html += f"<div style='width: 25px; height: 25px; background-color: {color}; border-radius: 3px;'></div>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)
