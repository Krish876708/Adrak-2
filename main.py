from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivy.uix.anchorlayout import AnchorLayout

# --- Configuration for Colors ---
BG_COLOR = get_color_from_hex('#1e272e')      
INPUT_BG = get_color_from_hex('#d2dae2')      
BTN_COLOR = get_color_from_hex('#0be881')     
CLEAR_BTN_COLOR = get_color_from_hex('#ff3f34') 
TEXT_COLOR = get_color_from_hex('#ffffff')    
ACCENT_COLOR = get_color_from_hex('#00d8d6')  
ERROR_COLOR = get_color_from_hex('#ff3f34')   
LABEL_COLOR = get_color_from_hex('#ffdd59')   

class AdrakMattiApp(App):
    def build(self):
        Window.clearcolor = BG_COLOR
        self.title = "Adrak Matti Calculator"

        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # --- Header Section ---
        header = Label(
            text="Adrak Matti Calculator ", 
            font_size='26sp', 
            bold=True, 
            color=ACCENT_COLOR,
            size_hint_y=None, 
            height=60
        )
        self.main_layout.add_widget(header)

        # --- Inputs Section ---
        input_scroll = ScrollView(size_hint=(1, 0.45))
        
        self.input_grid = GridLayout(cols=2, spacing=15, size_hint_y=None, padding=[10, 10])
        self.input_grid.bind(minimum_height=self.input_grid.setter('height'))

        lbl_target = Label(text="Total (Matti)", font_size='22sp', bold=True, color=ACCENT_COLOR, size_hint_y=None, height=90)
        self.input_grid.add_widget(lbl_target)
        
        self.target_input = TextInput(
            multiline=False, input_filter='int', write_tab=False,
            background_color=[1, 1, 0.8, 1], font_size='24sp', hint_text="Sum",
            padding_y=[20, 0], size_hint_y=None, height=100
        )
        self.input_grid.add_widget(self.target_input)
        
        self.inputs = []
        for i in range(1, 21):
            lbl = Label(text=f"Num {i}", font_size='18sp',bold=True, color=TEXT_COLOR, size_hint_y=None, height=70)
            self.input_grid.add_widget(lbl)
            
            ti = TextInput(
                multiline=False, input_filter='int', write_tab=False, 
                background_color=INPUT_BG, font_size='20sp', hint_text="0",
                padding_y=[15, 0], size_hint_y=None, height=100
            )
            self.input_grid.add_widget(ti)
            self.inputs.append(ti)
            
        input_scroll.add_widget(self.input_grid)
        self.main_layout.add_widget(input_scroll)
        
        # --- Action Buttons ---
        calc_btn = Button(
            text="CALCULATE MATCH", font_size='20sp', bold=True,
            size_hint_y=None, height=70, background_normal='', 
            background_color=BTN_COLOR, color=[0, 0, 0, 1] 
        )
        calc_btn.bind(on_press=self.run_search_logic)
        self.main_layout.add_widget(calc_btn)

        clear_container = AnchorLayout(anchor_x='right', size_hint_y=None, height=90)
        clear_btn = Button(
            text="CLEAR ALL", font_size='16sp', bold=True,
            size_hint=(None, None), size=(250, 50),
            background_normal='', background_color=CLEAR_BTN_COLOR, color=[1, 1, 1, 1]
        )
        clear_btn.bind(on_press=self.clear_fields)
        clear_container.add_widget(clear_btn)
        self.main_layout.add_widget(clear_container)
        
        # --- Results Section ---
        result_scroll = ScrollView(size_hint=(1, 0.4))
        self.result_label = Label(
            text="Result Waiting...", font_size='18sp',
            markup=True, halign="left", valign="top", size_hint_y=None, padding=[20, 20]
        )
        self.result_label.bind(texture_size=self._update_label_height)
        self.result_label.bind(width=lambda *x: self.result_label.setter('text_size')(self.result_label, (self.result_label.width, None)))
        
        result_scroll.add_widget(self.result_label)
        self.main_layout.add_widget(result_scroll)
        
        return self.main_layout

    def clear_fields(self, instance):
        self.target_input.text = ""
        for ti in self.inputs:
            ti.text = ""
        self.result_label.text ="Result Waiting... "

    def _update_label_height(self, instance, size):
        instance.height = size[1]

    def run_search_logic(self, instance):
        self.result_label.text = f"[color=#f1c40f]Calculating... please wait[/color]"
        try:
            get_val = lambda x: int(x) if x and x.strip() else 0
            totals = [get_val(ti.text) for ti in self.inputs]
            original_target = get_val(self.target_input.text)
            
            if original_target == 0 and all(t == 0 for t in totals):
                self.result_label.text = f"[color={self._hex(ERROR_COLOR)}]Input khali hai![/color]"
                return

            # Pehle original target check hoga, fir target + 1
            target_list = [original_target, original_target + 1]
            found = False

            for target_sum in target_list:
                if found: break
                
                for counter in range(1, 1000000):
                    current_value = counter / 1000.0
                    calculated_parts = [int(t / current_value) for t in totals]
                    sum_total = sum(calculated_parts)
                    
                    if sum_total == target_sum:
                        found = True
                        result_rows = []
                        for idx in range(20):
                            if totals[idx] > 0:
                                row = f"T{idx+1}: {totals[idx]} - Matti: {calculated_parts[idx]} = [b][color={self._hex(ACCENT_COLOR)}]{int(totals[idx] - calculated_parts[idx])}[/color][/b]"
                                result_rows.append(row)
                        
                        # Notification agar +1 use hua hai
                        status_msg = ""
                        if target_sum > original_target:
                            status_msg = f"[color={self._hex(ERROR_COLOR)}][b](Adjusted: Total + 1)[/b][/color]\n"

                        self.result_label.text = (
                            f"[b][color={self._hex(BTN_COLOR)}][size=30]MATCH FOUND![/size][/color][/b]\n"
                            f"{status_msg}"
                            f"[color={self._hex(LABEL_COLOR)}]Divisor:[/color] [b][size=40]{current_value}[/size][/b]\n"
                            f"[color=#7f8c8d]──────────────────────────────[/color]\n"
                            f"{'\n'.join(result_rows)}\n\n"
                            f"[color={self._hex(TEXT_COLOR)}]Total Matti pluse: {sum_total}[/color]"
                        )
                        break
            
            if not found:
                self.result_label.text = f"[color={self._hex(ERROR_COLOR)}][b]No Match Found even with +1[/b][/color]"
        except Exception as e:
            self.result_label.text = f"[color={self._hex(ERROR_COLOR)}]Error: {str(e)}[/color]"

    def _hex(self, color_list):
        r, g, b, a = color_list
        return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

if __name__ == '__main__':
    AdrakMattiApp().run()