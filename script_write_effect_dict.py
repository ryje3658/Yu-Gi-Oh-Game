import gc
from cards import *

unique_effect_cards = []
output_string = "{"

for obj in gc.get_objects():
    if isinstance(obj, Card):
        if obj.effect:
            unique_effect_cards.append(obj)

for obj in set(unique_effect_cards):
    function_string = str(obj.name).lower().replace(' ', '_').replace('-', '_').replace('.', '') + "_eff"
    obj_string = "\"" + obj.name + "\""
    output_string = output_string + f"{obj_string}: {function_string}, "

output_string = output_string + "}"

print(output_string)
