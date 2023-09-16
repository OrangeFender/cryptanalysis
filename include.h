#include<list>
#include<string>
#include<fstream>

int rotors_and_reflector(int input, int mid_key, int quick_key);
bool ** find_possible_key(int loop_length, int * characteristic_array);
class Key_Stecker{
    public:
    int mid_key;
    int quick_key;
    int stecker[26];
    int stecker_link_number=0;

    Key_Stecker(int mid_key, int quick_key);
};
std::list<Key_Stecker*>* step1_select_valid_key(bool **key);
std::list<Key_Stecker *> *step2_delete_invalid_key(std::list<Key_Stecker *> *key_stecker_list_pre, int loop_length, int *characteristic_array, std::string plain);
void encrypt(Key_Stecker* ks_all, std::string plain, int length, std::ofstream * output);