import random
import numpy as np
from manim import *


random.seed(1)

class MainCycle(Scene):
    
    def construct(self):
        # define the blocks as dictionaries with the keys "text" and "color"
        blocks = [
            {"text": "Audio Recording and Transcription", "color": BLUE},
            {"text": "Command Search", "color": GREEN},
            {"text": "Command Execution", "color": ORANGE},
            {"text": "Response to Speech", "color": PURPLE},
        ]
        
        # define the positions of the blocks in a polygon
        num_blocks = len(blocks)
        radius = 2
        angles = [PI/2 + 2 * PI * i / num_blocks for i in range(num_blocks)]
        positions = [radius * np.array([np.cos(angle), np.sin(angle), 0]) for angle in angles]
        
        # create the blocks and labels
        blocks_group = VGroup()
        labels_group = VGroup()
        for i in range(num_blocks):
            # block = Circle(fill_opacity=1, fill_color=blocks[i]["color"], stroke_width=0).move_to(positions[i])
            label = Text(blocks[i]["text"], color=WHITE)\
                .move_to(positions[i]) \
                .scale(0.3)
            # blocks_group.add(block)
            labels_group.add(label)
        
        # create the arrows between the blocks
        arrows_group = VGroup()
        for i in range(num_blocks):
            arrow = Arrow(
                start=positions[i], 
                end=positions[(i+1) % num_blocks], 
                stroke_width=3, 
                buff=0.25, 
                color=WHITE
            )
            arrows_group.add(arrow)
        
        # animate the blocks, labels, and arrows
        self.play(Create(blocks_group), Create(labels_group))
        self.wait()
        self.play(Create(arrows_group))
        self.wait()
        
class MainScheme(Scene):
    
    def construct(self):
        r = 0.5
        s = 0.5
        # Define the blocks
        audio_block = Rectangle(height=r, width=r, fill_color=BLUE, fill_opacity=0.8)
        audio_block_label = Text("Audio Recording\n& Transcription").scale(s)
        audio_block_group = VGroup(audio_block, audio_block_label).arrange(DOWN)
        
        search_block = Rectangle(height=r, width=r, fill_color=YELLOW, fill_opacity=0.8)
        search_block_label = Text("Command\nSearch").scale(s)
        search_block_group = VGroup(search_block, search_block_label).arrange(DOWN)
        
        execute_block = Rectangle(height=r, width=r, fill_color=GREEN, fill_opacity=0.8)
        execute_block_label = Text("Command\nExecution").scale(s)
        execute_block_group = VGroup(execute_block, execute_block_label).arrange(DOWN)
        
        response_block = Rectangle(height=r, width=r, fill_color=RED, fill_opacity=0.8)
        response_block_label = Text("Response to\n Speech").scale(s)
        response_block_group = VGroup(response_block, response_block_label).arrange(DOWN)
        
        # Define the arrows
        arrow = Arrow(start=LEFT, end=RIGHT)
        # search_to_execute_arrow = Arrow(search_block.get_bottom(), execute_block.get_top())
        # execute_to_response_arrow = Arrow(execute_block.get_bottom(), response_block.get_top())
        # response_to_audio_arrow = Arrow(response_block.get_left(), audio_block.get_right())
        
        # Group the blocks and arrows together
        diagram = VGroup(
            audio_block_group,
            arrow,
            search_block_group,
            arrow.copy(),
            execute_block_group,
            arrow.copy(),
            response_block_group,
        ).arrange(RIGHT, buff=0)
        
        self.play(Create(diagram))
        self.wait(2)

class Levenshtein(Scene):
    
    def construct(self):
        full = MathTex(r'''\operatorname{d}_{a,b}(i, j) = 
\begin{cases}
  j & \text{if } i = 0\\
  i & \text{if } j = 0\\
  \operatorname{d}_{a,b}(i-1, j-1) & \text{if } a_i = b_j\\
  1 + \min \begin{cases}
    \operatorname{d}_{a,b}(i-1, j)\\
    \operatorname{d}_{a,b}(i, j-1)\\
    \operatorname{d}_{a,b}(i-1, j-1)\\
    \operatorname{d}_{a,b}(i-2, j-2) + 1 & \text{if } i > 1, j > 1, a_i = b_{j-1} \text{ and } a_{i-1} = b_j
  \end{cases} & \text{otherwise}
\end{cases}''').scale(0.65) 
        
        insert = MathTex(r'\text{Insertion: } \operatorname{d}_{a,b}(i, j) = \operatorname{d}_{a,b}(i, j-1) + 1')
        
        delete = MathTex(r'\text{Deletion: } \operatorname{d}_{a,b}(i, j) = \operatorname{d}_{a,b}(i-1, j) + 1') \
            .next_to(insert, DOWN)
        
        replace = MathTex(r'\text{Replacement: } \operatorname{d}_{a,b}(i, j) = \operatorname{d}_{a,b}(i-1, j-1) + 1') \
            .next_to(delete, DOWN)
        
        transpose = MathTex(r'\text{Transposition: } \operatorname{d}_{a,b}(i, j) = \operatorname{d}_{a,b}(i-2, j-2) + 1') \
            .next_to(replace, DOWN)
        
        # self.play(Write(full))
        self.add(full)
        
        self.wait(1)
        
        self.play(Transform(full, insert))
        self.play(Transform(insert.copy(), delete))
        self.play(Transform(delete.copy(), replace))
        self.play(Transform(replace.copy(), transpose))

        # highlighted = full[0][114:156]
        # highlighted.set_color(YELLOW)
        # self.play(FocusOn(highlighted))
        
        self.wait(1)
        
class LevenshteinTable(Scene):
    
    def construct(self):
        a = "Sunday"
        b = "Saturday"
        n = len(a)
        m = len(b)
        
        # Initialize the table with empty entries
        table = [[0 for _ in range(m+1)] for _ in range(n+1)]
        path = []
        
        # Fill in the base cases
        for i in range(n+1):
            table[i][0] = i
        for j in range(m+1):
            table[0][j] = j
        
        # Fill in the remaining entries
        for i in range(1, n+1):
            for j in range(1, m+1):
                if a[i-1] == b[j-1]:
                    table[i][j] = table[i-1][j-1]
                    continue
                else:
                    insertion = table[i][j-1]
                    deletion = table[i-1][j]
                    substitution = table[i-1][j-1]
                    table[i][j] = min(insertion, deletion, substitution) + 1
                
        i = n
        j = m
        while i > 0 or j > 0:
            path.append((i, j))
            insertion = table[i][j-1]
            deletion = table[i-1][j]
            substitution = table[i-1][j-1]
            minimal = min(insertion, deletion, substitution)
            if minimal == substitution:
                i -= 1
                j -= 1
            elif minimal == insertion:
                j -= 1
            elif minimal == deletion:
                i -= 1

        # to str
        
        table = [[str(c) for c in l] for l in table]
                    
        for i, row in enumerate(table):
            if i < 1:
                row.insert(0, '')
                continue
            row.insert(0, a[i-1])
            
        table.insert(0, ['', ''] + list(b))
        
        # draw
        
        table_v = Table(table, include_outer_lines=True, h_buff=1, v_buff=1).scale(0.5)
        self.play(Write(table_v))
        
        # highlight path
        
        for i, j in path:
            i = (i + 2) % (n + 2)
            j = (j + 2) % (m + 2)
            table_v.add_highlighted_cell((i, j), color = YELLOW)
        
        self.wait(3)
        
class Command(Scene):
    
    def construct(self):
        self.play(Write(Tex('qwerty')))

class Perceptron(Scene):
    def construct(self):
        input_layer = VGroup()
        for i in range(1, 4):
            circle = Circle(radius=0.3, fill_opacity=1, color=WHITE).shift(LEFT*2 + UP*(i-1))
            input_layer.add(circle)

        hidden_layer = VGroup()
        for i in range(1, 4):
            circle = Circle(radius=0.3, fill_opacity=1, color=WHITE).shift(UP*(i-1))
            hidden_layer.add(circle)

        output_layer = VGroup()
        for i in range(1, 3):
            circle = Circle(radius=0.3, fill_opacity=1, color=WHITE).shift(RIGHT*2 + UP*(i-1) + UP*0.5)
            output_layer.add(circle)
        
        arrows1 = VGroup()
        for i in range(1, 4):
            for j in range(1, 4):
                if not random.randint(0, 3):
                    continue
                arrows1.add(
                    Arrow(input_layer[i-1].get_right(), hidden_layer[j-1].get_left(), buff=0.1, color=WHITE, tip_length=0.1, stroke_width=2)
                )
        
        arrows2 = VGroup()
        for i in range(1, 4):
            for j in range(1, 3):
                if not random.randint(0, 10):
                    continue
                arrows2.add(
                    Arrow(hidden_layer[i-1].get_right(), output_layer[j-1].get_left(), buff=0.1, color=WHITE, tip_length=0.1, stroke_width=2)
                )
                
        perceptron = VGroup(input_layer, hidden_layer, output_layer, arrows1, arrows2)
        
        self.add(perceptron)
        self.wait(1)

class Algorithm(Scene):
    def construct(self):
        rect1 = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.5) \
            .to_edge(UP, buff=0.5)
                   
        rhombus1 = Polygon(
            UP* 0.5, 
            RIGHT * 1, 
            DOWN * 0.5, 
            LEFT * 1,
            color=WHITE,
            fill_opacity=0.5,
            stroke_width=2,
            stroke_color=WHITE
        ).next_to(rect1, direction=DOWN, buff=1)
        
        rect2 = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.5) \
            .next_to(rhombus1, direction=DR, buff=0.25)
        
        rect3 = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.5) \
            .next_to(rhombus1, direction=DL, buff=0.25)
        
        arrow1 = Arrow(rect1.get_bottom(), rhombus1.get_top(), buff=0.1, color=WHITE, tip_length=0.1, stroke_width=2)

        arrow2 = Arrow(rhombus1.get_right(), rect2.get_top(), buff=0.1, color=WHITE, tip_length=0.1, stroke_width=2)

        arrow3 = Arrow(rhombus1.get_left(), rect3.get_top(), buff=0.1, color=WHITE, tip_length=0.1, stroke_width=2)
        
        self.add(rect1, rhombus1, rect2, rect3, arrow1, arrow2, arrow3)
        self.wait(1)


