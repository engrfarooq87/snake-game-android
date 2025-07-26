from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.popup import Popup
import random


class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        
        # Game settings
        self.grid_size = 20
        self.game_speed = 0.15  # seconds between moves
        
        # Game state
        self.snake = [(10, 10)]  # Snake body positions
        self.direction = (1, 0)  # Moving right initially
        self.food = self.generate_food()
        self.score = 0
        self.game_running = False
        self.game_over = False
        
        # Colors
        self.bg_color = (0.1, 0.1, 0.1, 1)  # Dark gray
        self.snake_color = (0, 0.8, 0, 1)   # Green
        self.food_color = (0.8, 0, 0, 1)    # Red
        self.grid_color = (0.2, 0.2, 0.2, 1)  # Light gray
        
        # UI setup
        self.setup_ui()
        
        # Bind touch events
        self.bind(on_touch_down=self.on_touch_down)
        
        # Game loop
        self.game_event = None
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Top bar with score and controls
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        
        # Score label
        self.score_label = Label(
            text=f'Score: {self.score}',
            font_size='20sp',
            size_hint_x=0.5,
            color=(1, 1, 1, 1)
        )
        top_bar.add_widget(self.score_label)
        
        # Control buttons
        self.start_btn = Button(
            text='Start Game',
            size_hint_x=0.25,
            background_color=(0, 0.7, 0, 1)
        )
        self.start_btn.bind(on_press=self.start_game)
        top_bar.add_widget(self.start_btn)
        
        self.pause_btn = Button(
            text='Pause',
            size_hint_x=0.25,
            background_color=(0.7, 0.7, 0, 1),
            disabled=True
        )
        self.pause_btn.bind(on_press=self.toggle_pause)
        top_bar.add_widget(self.pause_btn)
        
        main_layout.add_widget(top_bar)
        
        # Game area
        self.game_area = Widget()
        main_layout.add_widget(self.game_area)
        
        # Control buttons for mobile
        controls_layout = GridLayout(cols=3, rows=3, size_hint_y=0.3, spacing=5)
        
        # Create directional buttons
        controls_layout.add_widget(Widget())  # Empty space
        
        up_btn = Button(text='↑', font_size='30sp', background_color=(0.3, 0.3, 0.7, 1))
        up_btn.bind(on_press=lambda x: self.change_direction((0, 1)))
        controls_layout.add_widget(up_btn)
        
        controls_layout.add_widget(Widget())  # Empty space
        
        left_btn = Button(text='←', font_size='30sp', background_color=(0.3, 0.3, 0.7, 1))
        left_btn.bind(on_press=lambda x: self.change_direction((-1, 0)))
        controls_layout.add_widget(left_btn)
        
        controls_layout.add_widget(Widget())  # Center space
        
        right_btn = Button(text='→', font_size='30sp', background_color=(0.3, 0.3, 0.7, 1))
        right_btn.bind(on_press=lambda x: self.change_direction((1, 0)))
        controls_layout.add_widget(right_btn)
        
        controls_layout.add_widget(Widget())  # Empty space
        
        down_btn = Button(text='↓', font_size='30sp', background_color=(0.3, 0.3, 0.7, 1))
        down_btn.bind(on_press=lambda x: self.change_direction((0, -1)))
        controls_layout.add_widget(down_btn)
        
        controls_layout.add_widget(Widget())  # Empty space
        
        main_layout.add_widget(controls_layout)
        
        # Instructions
        instructions = Label(
            text='Swipe or use buttons to control the snake!\nEat red food to grow and score points.',
            font_size='14sp',
            size_hint_y=0.1,
            text_size=(None, None),
            halign='center',
            color=(0.7, 0.7, 0.7, 1)
        )
        main_layout.add_widget(instructions)
        
        self.add_widget(main_layout)
        
    def generate_food(self):
        """Generate food at random position"""
        while True:
            x = random.randint(1, self.get_grid_width() - 2)
            y = random.randint(1, self.get_grid_height() - 2)
            if (x, y) not in self.snake:
                return (x, y)
                
    def get_grid_width(self):
        """Get grid width based on screen size"""
        return max(20, int(self.game_area.width / self.grid_size))
        
    def get_grid_height(self):
        """Get grid height based on screen size"""
        return max(15, int(self.game_area.height / self.grid_size))
        
    def start_game(self):
        """Start or restart the game"""
        # Reset game state
        self.snake = [(10, 10)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_running = True
        
        # Update UI
        self.score_label.text = f'Score: {self.score}'
        self.start_btn.text = 'Restart'
        self.start_btn.background_color = (0.7, 0.5, 0, 1)
        self.pause_btn.disabled = False
        
        # Start game loop
        if self.game_event:
            self.game_event.cancel()
        self.game_event = Clock.schedule_interval(self.update_game, self.game_speed)
        
        # Redraw
        self.draw_game()
        
    def toggle_pause(self):
        """Toggle game pause"""
        if self.game_running:
            self.game_running = False
            self.pause_btn.text = 'Resume'
            self.pause_btn.background_color = (0, 0.7, 0, 1)
            if self.game_event:
                self.game_event.cancel()
        else:
            self.game_running = True
            self.pause_btn.text = 'Pause'
            self.pause_btn.background_color = (0.7, 0.7, 0, 1)
            self.game_event = Clock.schedule_interval(self.update_game, self.game_speed)
            
    def change_direction(self, new_direction):
        """Change snake direction"""
        if not self.game_running or self.game_over:
            return
            
        # Prevent reversing into itself
        current_dir = self.direction
        if (new_direction[0] == -current_dir[0] and new_direction[1] == -current_dir[1]):
            return
            
        self.direction = new_direction
        
    def update_game(self, dt):
        """Main game update loop"""
        if not self.game_running or self.game_over:
            return False
            
        # Move snake
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check collisions
        if self.check_collision(new_head):
            self.end_game()
            return False
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.score_label.text = f'Score: {self.score}'
            self.food = self.generate_food()
            
            # Increase speed slightly
            if self.score % 50 == 0 and self.game_speed > 0.05:
                self.game_speed -= 0.01
                if self.game_event:
                    self.game_event.cancel()
                self.game_event = Clock.schedule_interval(self.update_game, self.game_speed)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
        # Redraw game
        self.draw_game()
        return True
        
    def check_collision(self, pos):
        """Check if position collides with walls or snake body"""
        x, y = pos
        
        # Wall collision
        if (x < 0 or x >= self.get_grid_width() or 
            y < 0 or y >= self.get_grid_height()):
            return True
            
        # Self collision
        if pos in self.snake:
            return True
            
        return False
        
    def end_game(self):
        """End the game"""
        self.game_over = True
        self.game_running = False
        
        if self.game_event:
            self.game_event.cancel()
            
        # Update UI
        self.start_btn.text = 'Play Again'
        self.start_btn.background_color = (0, 0.7, 0, 1)
        self.pause_btn.disabled = True
        
        # Show game over popup
        self.show_game_over_popup()
        
    def show_game_over_popup(self):
        """Show game over popup"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        title = Label(
            text='Game Over!',
            font_size='24sp',
            size_hint_y=0.3,
            color=(1, 0.2, 0.2, 1)
        )
        content.add_widget(title)
        
        score_text = Label(
            text=f'Final Score: {self.score}',
            font_size='18sp',
            size_hint_y=0.3,
            color=(1, 1, 1, 1)
        )
        content.add_widget(score_text)
        
        # High score message
        high_score_msg = "New High Score!" if self.score > 0 else "Try again!"
        msg_label = Label(
            text=high_score_msg,
            font_size='16sp',
            size_hint_y=0.2,
            color=(0.8, 0.8, 0.8, 1)
        )
        content.add_widget(msg_label)
        
        close_btn = Button(
            text='OK',
            size_hint_y=0.2,
            background_color=(0, 0.7, 0, 1)
        )
        content.add_widget(close_btn)
        
        popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        
    def draw_game(self):
        """Draw the game graphics"""
        self.game_area.canvas.clear()
        
        if not self.game_area.width or not self.game_area.height:
            return
            
        with self.game_area.canvas:
            # Background
            Color(*self.bg_color)
            Rectangle(pos=self.game_area.pos, size=self.game_area.size)
            
            # Calculate cell size
            cell_width = self.game_area.width / self.get_grid_width()
            cell_height = self.game_area.height / self.get_grid_height()
            
            # Draw grid lines
            Color(*self.grid_color)
            for i in range(self.get_grid_width() + 1):
                x = self.game_area.x + i * cell_width
                Rectangle(pos=(x, self.game_area.y), size=(1, self.game_area.height))
            for i in range(self.get_grid_height() + 1):
                y = self.game_area.y + i * cell_height
                Rectangle(pos=(self.game_area.x, y), size=(self.game_area.width, 1))
            
            # Draw snake
            Color(*self.snake_color)
            for i, (x, y) in enumerate(self.snake):
                # Make head slightly different
                if i == 0:
                    Color(0, 1, 0, 1)  # Brighter green for head
                else:
                    Color(*self.snake_color)
                    
                rect_x = self.game_area.x + x * cell_width + 1
                rect_y = self.game_area.y + y * cell_height + 1
                Rectangle(
                    pos=(rect_x, rect_y),
                    size=(cell_width - 2, cell_height - 2)
                )
            
            # Draw food
            Color(*self.food_color)
            food_x = self.game_area.x + self.food[0] * cell_width + 2
            food_y = self.game_area.y + self.food[1] * cell_height + 2
            Rectangle(
                pos=(food_x, food_y),
                size=(cell_width - 4, cell_height - 4)
            )
            
    def on_touch_down(self, touch):
        """Handle touch input for swipe controls"""
        if not self.game_area.collide_point(*touch.pos):
            return super(SnakeGame, self).on_touch_down(touch)
            
        if not self.game_running or self.game_over:
            return super(SnakeGame, self).on_touch_down(touch)
            
        # Store touch start position
        touch.grab_current = self
        self.touch_start = touch.pos
        return True
        
    def on_touch_up(self, touch):
        """Handle touch release for swipe detection"""
        if touch.grab_current is not self:
            return super(SnakeGame, self).on_touch_up(touch)
            
        if not hasattr(self, 'touch_start'):
            return super(SnakeGame, self).on_touch_up(touch)
            
        # Calculate swipe direction
        dx = touch.pos[0] - self.touch_start[0]
        dy = touch.pos[1] - self.touch_start[1]
        
        # Minimum swipe distance
        min_swipe = 50
        
        if abs(dx) > abs(dy) and abs(dx) > min_swipe:
            # Horizontal swipe
            if dx > 0:
                self.change_direction((1, 0))  # Right
            else:
                self.change_direction((-1, 0))  # Left
        elif abs(dy) > min_swipe:
            # Vertical swipe
            if dy > 0:
                self.change_direction((0, 1))  # Up
            else:
                self.change_direction((0, -1))  # Down
                
        touch.ungrab(self)
        return True
        
    def on_size(self, *args):
        """Handle window resize"""
        if hasattr(self, 'game_area'):
            Clock.schedule_once(lambda dt: self.draw_game(), 0.1)


class SnakeApp(App):
    def build(self):
        # Set window properties
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        
        # Create and return the game
        game = SnakeGame()
        
        # Bind size events
        Window.bind(on_resize=game.on_size)
        
        return game
        
    def on_start(self):
        """Called when the app starts"""
        # Draw initial game state
        Clock.schedule_once(lambda dt: self.root.draw_game(), 0.1)


if __name__ == '__main__':
    SnakeApp().run()
