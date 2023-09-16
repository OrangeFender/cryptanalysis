#include<list>
int rotors_and_reflector(int input, int quick_key, int mid_key);
bool ** find_possible_key(int loop_length, int * characteristic_array);
class Key_Stecker{
    public:
    int key[2];
    int stecker[26];
    int stecker_link_number=0;

    Key_Stecker(int mid_key, int quick_key);
};
std::list<Key_Stecker*>* step1_select_valid_key(bool **key);