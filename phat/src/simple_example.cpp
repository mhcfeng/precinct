/*  Copyright 2013 IST Austria
    Contributed by: Ulrich Bauer, Michael Kerber, Jan Reininghaus

    This file is part of PHAT.

    PHAT is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PHAT is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with PHAT.  If not, see <http://www.gnu.org/licenses/>. */

// This file contains a simple example that demonstrates the usage of the library interface

// wrapper algorithm that computes the persistence pairs of a given boundary matrix using a specified algorithm
#include <phat/compute_persistence_pairs.h>

// main data structure (choice affects performance)
#include <phat/representations/vector_vector.h>

// algorithm (choice affects performance)
#include <phat/algorithms/standard_reduction.h>
#include <phat/algorithms/chunk_reduction.h>
#include <phat/algorithms/row_reduction.h>
#include <phat/algorithms/twist_reduction.h>

#include <fstream>
#include <iostream>

int main( int argc, char** argv )
{
    if( argc!=4 || ( strcmp(argv[2],"hillary")!=0 && strcmp(argv[2],"trump")!=0 ) || ( strcmp(argv[3],"rips")!=0 && strcmp(argv[3],"adj")!=0 && strcmp(argv[3],"alpha")!=0 && strcmp(argv[3],"ls")!=0) ) {
      std::cout << "Syntax: ./simple_example county candidate sctype" << std::endl;
      return -1;
    }
    // first define a boundary matrix with the chosen internal representation
    phat::boundary_matrix< phat::vector_vector > boundary_matrix;
    bool read_successful;
    std::string currcandidate=std::string( argv[2] );
    std::string currcounty=std::string( argv[1] );
    std::string sctype=std::string( argv[3] );

    std::string inputfilename = "../data/sc/"+sctype+"/"+currcandidate+"/"+currcounty+".dat";
    //std::string inputfilename = "examples/triangle.dat";

    read_successful = boundary_matrix.load_ascii( inputfilename );


    // define the object to hold the resulting persistence pairs
    phat::persistence_pairs pairs;
    phat::boundary_matrix< phat::vector_vector > changes;

    // choose an algorithm (choice affects performance) and compute the persistence pair
    // (modifies boundary_matrix)
    phat::compute_persistence_pairs< phat::twist_reduction >( pairs, boundary_matrix, changes );

    // sort the persistence pairs by birth index
    pairs.sort();




    std::vector <int> entry_times;
    std::ifstream infile( "../data/sc/"+sctype+"/"+currcandidate+"/"+currcounty+"_entry_times.csv" );
    std::string line;
    int x = 0;
    while(std::getline(infile,line)) {
      std::stringstream lineStream(line);
      std::string cell;
      while(std::getline(lineStream,cell,' ')) {
        entry_times.push_back(std::stoi(cell));
      }
    }

//    std::cout << std::endl;
//    std::cout << "There are " << pairs.get_num_pairs() << " persistence pairs: " << std::endl;
//    for( phat::index idx = 0; idx < pairs.get_num_pairs(); idx++ ) {
//        int birth = entry_times[pairs.get_pair( idx ).first];
//        int death = entry_times[pairs.get_pair( idx ).second];
//        if(birth!=death) {
//          std::cout << "Dimension: " << (int)boundary_matrix.get_dim(pairs.get_pair( idx ).first)<< ", Birth: " << birth << ", Death: " << death << ", Representative Cycle: ";
//          std::vector< phat::index > temp_col;
//          boundary_matrix.get_col( pairs.get_pair( idx ).second, temp_col );
//          for( phat::index idx = 0; idx < (phat::index)temp_col.size(); idx++ ) {
//              std::cout << " " << temp_col[ idx ];
//          }
//          std::cout << std::endl;
//
//        }
//      }


    std::string output_file="../results/"+sctype+"/"+currcandidate+"/"+currcounty+".csv";
    std::ofstream output;
    output.open( output_file );

    // print the pairs:
    //std::cout << std::endl;
    //std::cout << "There are " << pairs.get_num_pairs() << " persistence pairs: " << std::endl;
    int max_time = entry_times[entry_times.size()-1];
    for( phat::index idx = 0; idx < pairs.get_num_pairs(); idx++ ) {
        int birth = entry_times[pairs.get_pair( idx ).first];
        int death;
        if( pairs.get_pair( idx ).second < entry_times.size() ) {
          death = entry_times[pairs.get_pair( idx ).second];
        }
        else {
          death = max_time+1;
        }
        if( birth < death && (int)boundary_matrix.get_dim(pairs.get_pair( idx ).first)<2 ) {
          output << (int)boundary_matrix.get_dim(pairs.get_pair( idx ).first)<< "," << birth << "," << death << ",";
          std::vector< phat::index > temp_col;
          if( death < max_time+1 ) {
            boundary_matrix.get_col( pairs.get_pair( idx ).second, temp_col );
          }
          else {
            changes.get_col( pairs.get_pair( idx ).first, temp_col );
            output << pairs.get_pair( idx ).first << " ";
          }
          for( phat::index idx = 0; idx < (phat::index)temp_col.size(); idx++ ) {
              output << temp_col[ idx ] << " ";
          }
          output << std::endl;

        }
      }

      output.close();
      return 0;

}
