/******************************************************************************
This source code is licensed under the MIT license found in the
LICENSE file in the root directory of this source tree.
*******************************************************************************/

#ifndef __STATDATA_HH__
#define __STATDATA_HH__

#include <map>
#include <math.h>
#include <fstream>
#include <chrono>
#include <ctime>
#include <tuple>
#include <cstdint>
#include <list>
#include <vector>
#include <algorithm>
#include <chrono>
#include <sstream>
#include <assert.h>
#include "Common.hh"
#include "CallData.hh"
namespace AstraSim{
    class StatData:public CallData{
    public:
        Tick start;
        Tick waiting;
        Tick end;
        //~StatData()= default;
        StatData(){
            start=0;
            waiting=0;
            end=0;
        }
    };
}
#endif