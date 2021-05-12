Runebook_Gump_Id = 1431013363
Rune_Item_Id = 0x1F14

# Functions defined below.

# Recall, mark, name rune, add rune to book, repeat
def move_n_mark(rune_book_in_serial, rune_book_out_serial):
    global Rune_Item_Id
    global Runebook_Gump_Id
    
	#
    Items.UseItem(rune_book_in_serial)
    Gumps.WaitForGump(Runebook_Gump_Id, 10000)
    line_list =  Gumps.LastGumpGetLineList()[:]
    line_num = len(line_list)

    Gumps.WaitForGump(Runebook_Gump_Id, 10000)
    Gumps.SendAction( Runebook_Gump_Id, 0 )

    print( line_list )
    
    number_entries = 16
    
    for i in range(16):
        if line_list[line_num - i - 1] == "Empty":
            number_entries = number_entries - 1
	#
    
    print(number_entries)
    
    # Offset for looking in line list for rune name
    offset = 5 * ( number_entries + 1 )
    
	# NOTE: does not distinguish between marked and unmarked runes.
    runes_to_mark = find_items([Rune_Item_Id])
    
    if len(runes_to_mark) < number_entries:
        Player.HeadMessage(6, "Insufficient runes to copy entire runebook.")
        return -1
    
    for i in range(number_entries):
        Misc.Pause(2000)

        # Response indicating to recall to the next entry in the runebook
        gump_response_number = 5 + 6 * i

        # Recall to location in book
        Items.UseItem(rune_book_in_serial)
        Gumps.WaitForGump( Runebook_Gump_Id, 10000 )
        Gumps.SendAction( Runebook_Gump_Id, gump_response_number )
        
        Misc.Pause(2000)

        # Mark next rune in pack
        Spells.CastMagery("Mark")
        Target.WaitForTarget(10000, False)
        Target.TargetExecute(runes_to_mark[i])
        
        Misc.Pause(2000)

        # Rename rune just marked
        Items.UseItem(runes_to_mark[i])
        Misc.WaitForPrompt(10000)
        Misc.ResponsePrompt(line_list[offset + i])
        
        Misc.Pause(2000)

        # Move rune to new book
        Items.Move(runes_to_mark[i], rune_book_out_serial, 0)
#

#
def find_items(item_types, item_serial=Player.Backpack.Serial):
    found_items = []    
    cur_item = Items.FindBySerial(item_serial)
    
    # If the serial does not correspond to an item, no items can be found
    if not cur_item:
        return found_items

    # If I was looking for this item, add this item to the list of found items
    if cur_item.ItemID in item_types:
        found_items.append(cur_item)

    # If the item is not a container, no need to search within item for contained items
    if not cur_item.IsContainer:  
        return found_items

    # Otherwise, search inside of item for contained items
    
    # If current item is an empty container, it does not contain any items
    if len(cur_item.Contains) == 0:
        return found_items
    
    

    # Otherwise, look at all contained items and their potential contents with this same function for the same item types
    for item in cur_item.Contains:
        for contained_in_item in find_items(item_types, item.Serial):
            found_items.append(contained_in_item)
    return found_items
#


# All work is done here
###################################################################
filled_book_id = Target.PromptTarget("Target filled rune book.")
empty_book_id = Target.PromptTarget("Target empty rune book.")

move_n_mark(filled_book_id, empty_book_id)
###################################################################