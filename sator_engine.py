import numpy as np

class SatorEngine:
    def __init__(self):
        # The core 5x5 structural SATOR palindrome template matrix
        self.template = [
            ['S', 'A', 'T', 'O', 'R'],
            ['A', 'R', 'E', 'P', 'O'],
            ['T', 'E', 'N', 'E', 'T'],
            ['O', 'P', 'E', 'R', 'A'],
            ['R', 'O', 'T', 'A', 'S']
        ]
        self.matrix = np.array(self.template)

    def verify_symmetry(self, test_matrix):
        """
        Executes the S33 multi-directional verification check.
        Verifies that rows equal columns, and the matrix equals its full rotation.
        """
        # 1. Transpose Check: Rows must exactly match columns (A == A.T)
        is_transposed_equal = np.array_equal(test_matrix, test_matrix.T)
        
        # 2. Rotational Palindrome Check: Reading backwards/upside down must match (A == A rotated 180)
        # np.rot90(matrix, 2) flips both horizontally and vertically
        is_rotational_equal = np.array_equal(test_matrix, np.rot90(test_matrix, 2))
        
        if is_transposed_equal and is_rotational_equal:
            return True, "Symmetry Verified: State is Secure."
        else:
            return False, "CRITICAL ERROR: Symmetrical Matrix Fractured. Unauthorized Mutation Detected."

# --- MVP EXECUTION SIMULATION ---
if __name__ == "__main__":
    engine = SatorEngine()
    
    print("--- SATOR-33 (S33) COMPILATION SIMULATION ---")
    print("Initial Data Payload Layout:")
    print(engine.matrix)
    
    # Test 1: Clean State Verification
    is_valid, message = engine.verify_symmetry(engine.matrix)
    print(f"\n[Test 1 Run]: {message}")
    
    # Test 2: Simulating an External Malicious Attack or Exploit Injection
    tampered_matrix = engine.matrix.copy()
    tampered_matrix[1, 1] = 'X'  # Injecting an unexpected variant into the grid
    
    print("\nWarning: Hostile Payload Injected into Matrix:")
    print(tampered_matrix)
    
    is_valid_malicious, message_malicious = engine.verify_symmetry(tampered_matrix)
    print(f"\n[Test 2 Run]: {message_malicious}")
