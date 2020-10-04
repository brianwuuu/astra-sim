/******************************************************************************
Copyright (c) 2020 Georgia Institute of Technology
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author : Saeed Rashidi (saeed.rashidi@gatech.edu)
*******************************************************************************/

#ifndef __DOUBLEBINARYTREETOPOLOGY_HH__
#define __DOUBLEBINARYTREETOPOLOGY_HH__

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
#include "src/astra-sim/system/Common.hh"
#include "ComplexLogicalTopology.hh"
#include "LocalRingGlobalBinaryTree.hh"
namespace AstraSim{
    class DoubleBinaryTreeTopology:public ComplexLogicalTopology{
    public:
        int counter;
        LocalRingGlobalBinaryTree *DBMAX;
        LocalRingGlobalBinaryTree *DBMIN;
        LogicalTopology *get_topology();
        ~DoubleBinaryTreeTopology();
        DoubleBinaryTreeTopology(int id,int total_tree_nodes,int start,int stride,int local_dim);
    };
}
#endif