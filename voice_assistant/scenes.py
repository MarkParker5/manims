# import random
import numpy as np
from manim import *


# random.seed()
frame_height = config['frame_height']
frame_width = config['frame_width']

class NLP(Scene):
    def construct(self):
        
        title = Text('How it works?') \
            .scale(1.5)
            
        self.play(Write(title))
        self.wait(0.5)
        
        title2 = Title('Natural Language Processing') \
            .set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE) \
        
        self.play(Transform(title, title2))
        self.wait(1)
        
        algorithm_title = Text('Algorithmical') \
            .scale(0.5) \
            .move_to(UP * 0.25 * frame_height + LEFT * 0.25 * frame_width)
            
        algorithm = self.algorithm \
            .scale(0.5) \
            .move_to(LEFT * 0.25 * frame_width)
            
        perceptron_title = Text('Neural networks') \
            .scale(0.5) \
            .move_to(UP * 0.25 * frame_height + RIGHT * 0.25 * frame_width) \
            
        perceptron = self.perceptron \
            .scale(0.5) \
            .move_to(RIGHT * 0.25 * frame_width) \
            
        self.play(Write(algorithm_title))
        self.play(Write(algorithm))
        self.play(Write(perceptron_title))
        self.play(Write(perceptron))
        self.wait(1)
        
        self.play(
            FadeOut(title),
            FadeOut(algorithm),
            FadeOut(perceptron_title),
            FadeOut(perceptron),
            Transform(algorithm_title, Title('Algorithmical')),
        )
        
        self.wait(1)
        
        audio, search, execution, tts, arrows = self.main_cycle
        cycle = VGroup(audio, search, execution, tts)
        self.play(Write(cycle))
        self.wait(1)
        self.play(Write(arrows))
        
        self.play(search.animate.set_color(YELLOW), execution.animate.set_color(YELLOW))
        self.play(FocusOn(search), FocusOn(execution))
        
        self.wait(1)
        
        self.play(
            FadeOut(cycle),
            FadeOut(algorithm_title),
            FadeOut(arrows),
        )
        
    @property
    def algorithm(self) -> Mobject:
        rect1 = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.5)
                   
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
        
        return VGroup(rect1, rhombus1, rect2, rect3, arrow1, arrow2, arrow3)
        
    @property
    def perceptron(self) -> Mobject:
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
                arrows1.add(
                    Arrow(input_layer[i-1].get_right(), hidden_layer[j-1].get_left(), buff=0.1, color=WHITE, tip_length=0.1, stroke_width=2)
                )
        
        arrows2 = VGroup()
        for i in range(1, 4):
            for j in range(1, 3):
                arrows2.add(
                    Arrow(hidden_layer[i-1].get_right(), output_layer[j-1].get_left(), buff=0.1, color=WHITE, tip_length=0.1, stroke_width=2)
                )
                
        return VGroup(input_layer, hidden_layer, output_layer, arrows1, arrows2)
    
    @property
    def main_cycle(self) -> tuple[Mobject]:
        blocks = [
            {'text': 'Audio Recording and Transcription', 'color': BLUE},
            {'text': 'Command Search', 'color': GREEN},
            {'text': 'Command Execution', 'color': ORANGE},
            {'text': 'Response to Speech', 'color': PURPLE},
        ]
        
        # define the positions of the blocks in a polygon
        num_blocks = len(blocks)
        radius = 2.3
        angles = [PI/2 + 2 * PI * i / num_blocks for i in range(num_blocks)]
        positions = [radius * np.array([np.cos(angle), np.sin(angle), 0]) for angle in angles]
        
        # create the blocks and labels
        labels_group = VGroup()
        for i in range(num_blocks):
            label = Text(blocks[i]['text'], color=WHITE)\
                .move_to(positions[i]) \
                .scale(0.5)
            labels_group.add(label)
        
        # create the arrows between the blocks
        arrows_group = VGroup()
        for i in range(num_blocks):
            arrow = Arrow(
                start=positions[i], 
                end=positions[(i+1) % num_blocks], 
                stroke_width=3, 
                buff=0.5, 
                color=WHITE,
                tip_length=0.25
            )
            arrows_group.add(arrow)
        
        return [*labels_group.submobjects, arrows_group]

class Levenshtein(Scene):
    
    def construct(self):
        self.play(Write(Title('(Damerau-)Levenshtein Distance')))
        function = self.show_levenshtein_function()
        self.play(
            function.animate \
                .scale(0.6) \
                .move_to(UP * 0.25) \
                .to_edge(LEFT, buff=0.5) \
        )
        self.show_levenshtein_table()
        self.wait(3)
    
    def show_levenshtein_function(self) -> Mobject:
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
        
        self.play(Write(full))
        
        self.wait(1)
        
        self.play(Transform(full, insert))
        insert = full
        new_delete = insert.copy()
        self.play(Transform(new_delete, delete))
        delete = new_delete
        new_replace = delete.copy()
        self.play(Transform(new_replace, replace))
        replace = new_replace
        new_transpose = replace.copy()
        self.play(Transform(new_transpose, transpose))
        transpose = new_transpose

        # highlighted = full[0][114:156]
        # highlighted.set_color(YELLOW)
        # self.play(FocusOn(highlighted))
        
        self.wait(1)
        
        return VGroup(insert, delete, replace, transpose)
        
    def show_levenshtein_table(self) -> Mobject:
        a = 'Sunday'
        b = 'Saturday'
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
        
        table_v = Table(table, include_outer_lines=True, h_buff=1, v_buff=1) \
            .scale(0.4) \
            .to_edge(RIGHT, buff=0.5) \
            .set_z_index(1)
        
        for i in range(n + 2):
            i = (i + 1) % (n + 2)
            j = 1
            table_v.add_highlighted_cell((i, j), color=WHITE, fill_opacity=0.4)
            
        for j in range(1, m + 2):
            i = 1
            j = (j + 1) % (m + 2)
            table_v.add_highlighted_cell((i, j), color=WHITE, fill_opacity=0.4)

        self.play(Write(table_v))
        
        # highlight path
        
        for i, j in path:
            i = (i + 2) % (n + 2)
            j = (j + 2) % (m + 2)
            cell_to_highlight = table_v.get_cell((i, j))
            highlighted_cell = Rectangle(
                width=cell_to_highlight.get_width(),
                height=cell_to_highlight.get_height(),
                fill_color=YELLOW,
                fill_opacity=0.75,
                stroke_width=0
            ) \
            .move_to(cell_to_highlight) \
            .set_z_index(0)

            self.play(FadeIn(highlighted_cell), run_time=0.25)
        
        return table_v
        
class Command(Scene):
    
    def construct(self):
        code = Code(
            './snippet1.py',
            tab_width=4,
            background='window',
            style='one-dark'
        )
        
        code2 = Code(
            './snippet2.py',
            tab_width=4,
            background='none',
            style='one-dark'
        ).code.align_to(code.code, DL)
        
        self.play(Write(code), run_time=3)
        self.wait(2)
        self.play(Write(code2), run_time=1.5)
        
        group = VGroup(code, code2)
        
        self.wait(3)
        
class FindCommand(Scene):
    
    def construct(self):
        code = Code(
            './snippet3.py',
            tab_width=4,
            background='window',
            style='one-dark'
        ).scale(0.8)
        
        self.play(Write(code), run_time=3)
        self.wait(3)