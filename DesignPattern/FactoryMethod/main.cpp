#include "Restaurant.hpp"

int main(){
    cKorean     Korean1;
    cSushi      Sushi1;
    cChinese    Chinese1;
    cKorean     Korean2;
    cKorean     Korean3;
    cChinese    Chinese2;
    cChinese    Chinese3;
    cKorean     Korean4;

    cRestaurant* pStore1 = Korean1.incubateBussiness();
    cRestaurant* pStore2 = Sushi1.incubateBussiness();
    cRestaurant* pStore3 = Chinese1.incubateBussiness();
    cRestaurant* pStore4 = Korean2.incubateBussiness();
    cRestaurant* pStore5 = Korean3.incubateBussiness();
    cRestaurant* pStore6 = Chinese2.incubateBussiness();
    cRestaurant* pStore7 = Chinese3.incubateBussiness();
    cRestaurant* pStore8 = Korean4.incubateBussiness();

    pStore1->BussinessInfo();
    pStore2->BussinessInfo();
    pStore3->BussinessInfo();
    pStore4->BussinessInfo();
    pStore5->BussinessInfo();
    pStore6->BussinessInfo();
    pStore7->BussinessInfo();
    pStore8->BussinessInfo();
}