def extended_bottom_up_cut_rod(p, n):
    """
    Computes the maximum revenue r[j] and the optimal first-cut size s[j] 
    for a rod of length j, for j = 1 to n.

    Args:
        p (list): A list of prices where p[i] is the price of a rod of length i.
                  (p[0] is typically unused, so the list size is n+1).
        n (int): The total length of the rod.

    Returns:
        tuple: (r, s), where r is the array of maximum revenues and 
               s is the array of optimal first-cut sizes.
    """
    # Initialize arrays r and s of size n+1 (to account for length 0 to n)
    # Pseudocode Lines 1-2
    r = [0] * (n + 1)  # r[j] will store max revenue for length j
    s = [0] * (n + 1)  # s[j] will store the optimal first cut size for length j

    # Pseudocode Line 3: for j = 1 to n
    for j in range(1, n + 1):
        # Pseudocode Line 4: q D -infinity (using a very small number or -1 is safer, 
        # but 1 or 0 works if all p[i] >= 0, as in the pseudocode's context)
        # We'll use negative infinity to be robust, or simply p[1] + r[j-1] as the first candidate
        q = float('-inf')

        # Pseudocode Line 5: for i = 1 to j
        for i in range(1, j + 1):
            # Pseudocode Line 6: if q < p[i] + r[j - i]
            current_profit = p[i] + r[j - i]
            
            if q < current_profit:
                # Pseudocode Line 7: q D p[i] + r[j - i]
                q = current_profit
                
                # Pseudocode Line 8: s[j] D i
                s[j] = i
        
        # Pseudocode Line 9: r[j] D q
        r[j] = q
        
    # Pseudocode Line 10: return r and s
    return r, s

def print_cut_rod_solution(p, n):
    """
    Computes the optimal cuts and prints them out.

    Args:
        p (list): Price table.
        n (int): The total length of the rod.
    """
    
    print(f"--- Solving Cut-Rod Problem for Length {n} ---")
    
    # Pseudocode Line 1: (r, s) D EXTENDED-BOTTOM-UP-CUT-ROD(p, n)
    r, s = extended_bottom_up_cut_rod(p, n)
    
    total_revenue = r[n]
    
    print(f"Maximum Total Revenue: {total_revenue}")
    print("Optimal Cut Sequence:")
    
    # Pseudocode Line 2: while n > 0
    current_length = n
    cuts = []
    while current_length > 0:
        # The optimal first cut for the current length
        optimal_cut_size = s[current_length]
        
        # Pseudocode Line 3: print s[n]
        cuts.append(optimal_cut_size)
        
        # Pseudocode Line 4: n D n - s[n] (Update the remaining length)
        current_length -= optimal_cut_size
        
    print(" -> ".join(map(str, cuts)))

# Prices for lengths 0 through 8
# p[0] is unused, p[1]..p[8] are the actual prices
prices = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 26, 27, 39, 32, 34, 37]

for rod_length in range(len(prices)):
    print_cut_rod_solution(prices, rod_length)
