from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp

Window.clearcolor = (0.1, 0.1, 0.15, 1)


class HedgeApp(App):

    def build(self):
        self.title = "Hedge Calculator"
        root = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))

        # Title
        root.add_widget(Label(
            text="Arbitrage Hedge Calculator",
            font_size=dp(20),
            bold=True,
            size_hint_y=None,
            height=dp(44),
            color=(0.4, 0.9, 0.6, 1)
        ))

        # Form inputs
        form = GridLayout(cols=2, size_hint_y=None, height=dp(160), spacing=dp(8))

        form.add_widget(Label(
            text="Number of hedges:",
            halign='right',
            text_size=(dp(150), None)
        ))
        self.num_hedges_input = TextInput(
            text='2', multiline=False, input_filter='int',
            size_hint_y=None, height=dp(44),
            background_color=(0.2, 0.2, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.4, 0.9, 0.6, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        self.num_hedges_input.bind(text=self.on_num_hedges_change)
        form.add_widget(self.num_hedges_input)

        form.add_widget(Label(
            text="Total investment ($):",
            halign='right',
            text_size=(dp(150), None)
        ))
        self.budget_input = TextInput(
            hint_text='e.g. 100.00', multiline=False, input_filter='float',
            size_hint_y=None, height=dp(44),
            background_color=(0.2, 0.2, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.4, 0.9, 0.6, 1),
            hint_text_color=(0.5, 0.5, 0.5, 1)
        )
        form.add_widget(self.budget_input)

        root.add_widget(form)

        # Multiplier section header
        root.add_widget(Label(
            text="Multipliers (one per hedge):",
            size_hint_y=None, height=dp(28),
            halign='left', color=(0.7, 0.7, 0.7, 1),
            text_size=(Window.width - dp(32), None)
        ))

        # Scrollable multiplier inputs
        self.multiplier_container = BoxLayout(
            orientation='vertical', spacing=dp(6),
            size_hint_y=None
        )
        self.multiplier_container.bind(
            minimum_height=self.multiplier_container.setter('height')
        )
        scroll_m = ScrollView(size_hint=(1, None), height=dp(150))
        scroll_m.add_widget(self.multiplier_container)
        root.add_widget(scroll_m)

        self.multiplier_inputs = []
        self._build_multiplier_inputs(2)

        # Buttons row
        btn_row = BoxLayout(
            orientation='horizontal', size_hint_y=None,
            height=dp(50), spacing=dp(8)
        )
        calc_btn = Button(
            text="Calculate",
            background_color=(0.2, 0.6, 0.4, 1),
            font_size=dp(16), bold=True
        )
        calc_btn.bind(on_press=self.calculate)
        btn_row.add_widget(calc_btn)

        clear_btn = Button(
            text="Clear",
            background_color=(0.45, 0.18, 0.18, 1),
            font_size=dp(15),
            size_hint_x=0.35
        )
        clear_btn.bind(on_press=self.clear)
        btn_row.add_widget(clear_btn)
        root.add_widget(btn_row)

        # Results
        self.result_label = Label(
            text="Enter your hedges above and press Calculate.",
            size_hint_y=None,
            text_size=(Window.width - dp(32), None),
            halign='left', valign='top',
            color=(0.85, 0.85, 0.85, 1),
            font_size=dp(14),
            markup=True,
            padding=(0, dp(8))
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))

        result_scroll = ScrollView(size_hint=(1, 1))
        result_scroll.add_widget(self.result_label)
        root.add_widget(result_scroll)

        return root

    def _build_multiplier_inputs(self, count):
        self.multiplier_container.clear_widgets()
        self.multiplier_inputs = []
        example_odds = [2.1, 3.5, 4.2, 2.8, 5.0, 1.9, 3.3, 6.0]
        for i in range(count):
            row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None, height=dp(44),
                spacing=dp(8)
            )
            row.add_widget(Label(
                text=f"Hedge {i + 1}:",
                size_hint_x=0.35,
                halign='right',
                text_size=(dp(80), None)
            ))
            example = example_odds[i % len(example_odds)]
            ti = TextInput(
                hint_text=f'e.g. {example}',
                multiline=False, input_filter='float',
                size_hint_x=0.65,
                background_color=(0.2, 0.2, 0.28, 1),
                foreground_color=(1, 1, 1, 1),
                cursor_color=(0.4, 0.9, 0.6, 1),
                hint_text_color=(0.5, 0.5, 0.5, 1)
            )
            row.add_widget(ti)
            self.multiplier_container.add_widget(row)
            self.multiplier_inputs.append(ti)

    def on_num_hedges_change(self, instance, value):
        try:
            n = int(value)
            if 2 <= n <= 20:
                self._build_multiplier_inputs(n)
        except (ValueError, TypeError):
            pass

    def calculate(self, instance):
        try:
            budget_text = self.budget_input.text.strip()
            if not budget_text:
                self._show_error("Please enter a total investment amount.")
                return
            budget = float(budget_text)
            if budget <= 0:
                self._show_error("Investment must be greater than zero.")
                return

            multipliers = []
            for i, ti in enumerate(self.multiplier_inputs):
                val = ti.text.strip()
                if not val:
                    self._show_error(f"Please enter a multiplier for Hedge {i + 1}.")
                    return
                m = float(val)
                if m <= 1.0:
                    self._show_error(
                        f"Hedge {i + 1} multiplier must be greater than 1.0\n"
                        f"(You entered {m})"
                    )
                    return
                multipliers.append(m)

            # Arbitrage logic
            implied_probs = [1 / m for m in multipliers]
            total_implied = sum(implied_probs)

            if total_implied >= 1.0:
                self.result_label.color = (1, 0.4, 0.4, 1)
                self.result_label.text = (
                    "[b][color=ff5555]NO GOOD HEDGE[/color][/b]\n\n"
                    f"Combined implied probability: [b]{total_implied * 100:.2f}%[/b]\n"
                    "This must be [b]under 100%[/b] for an arb opportunity.\n\n"
                    f"You need to find better odds — currently "
                    f"over by {(total_implied - 1) * 100:.2f}%."
                )
                return

            # Profitable — calculate stakes
            margin = (1 - total_implied) * 100
            lines = [
                "[b][color=44ee88]PROFITABLE HEDGE FOUND[/color][/b]\n",
                f"Implied probability total: [b]{total_implied * 100:.2f}%[/b]",
                f"Arb margin: [b][color=44ee88]+{margin:.2f}%[/color][/b]\n",
                "[b]── Stakes ──[/b]"
            ]

            stakes = []
            for i, prob in enumerate(implied_probs):
                stake = budget * (prob / total_implied)
                stakes.append(stake)
                payout = stake * multipliers[i]
                lines.append(
                    f"Hedge {i + 1}  (x{multipliers[i]:.2f}):  "
                    f"[b]${stake:.2f}[/b]  →  returns ${payout:.2f}"
                )

            guaranteed_payout = stakes[0] * multipliers[0]
            net_profit = guaranteed_payout - budget

            lines += [
                "\n[b]── Summary ──[/b]",
                f"Total invested:        [b]${sum(stakes):.2f}[/b]",
                f"Guaranteed payout:     [b]${guaranteed_payout:.2f}[/b]",
                f"[color=44ee88][b]Net risk-free profit:  ${net_profit:.2f}[/b][/color]",
                f"Return on investment:  [b]{(net_profit / budget) * 100:.2f}%[/b]"
            ]

            self.result_label.color = (0.9, 0.9, 0.9, 1)
            self.result_label.text = "\n".join(lines)

        except ValueError:
            self._show_error("Invalid input — please enter numbers only.")

    def _show_error(self, msg):
        self.result_label.color = (1, 0.55, 0.3, 1)
        self.result_label.text = f"[b][color=ff8844]Error:[/color][/b]\n{msg}"

    def clear(self, instance):
        self.budget_input.text = ''
        for ti in self.multiplier_inputs:
            ti.text = ''
        self.result_label.text = "Enter your hedges above and press Calculate."
        self.result_label.color = (0.85, 0.85, 0.85, 1)


if __name__ == '__main__':
    HedgeApp().run()
