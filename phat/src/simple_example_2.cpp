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

int main( int argc, char** argv )
{
    // first define a boundary matrix with the chosen internal representation
    phat::boundary_matrix< phat::vector_vector > boundary_matrix;
    bool read_successful;

    read_successful = boundary_matrix.load_ascii( inputfilename );

    // print some information of the boundary matrix:
    /*std::cout << std::endl;
    std::cout << "The boundary matrix has " << boundary_matrix.get_num_cols() << " columns: " << std::endl;
    std::cout << "Overall, the boundary matrix has " << boundary_matrix.get_num_entries() << " entries." << std::endl;*/


    // define the object to hold the resulting persistence pairs
    phat::persistence_pairs pairs;

    // choose an algorithm (choice affects performance) and compute the persistence pair
    // (modifies boundary_matrix)
    phat::compute_persistence_pairs< phat::twist_reduction >( pairs, boundary_matrix );

    // sort the persistence pairs by birth index
    pairs.sort();

    std::vector <int> entry_times;
    std::ifstream infile( "../../precincts/data/simplicialcomplex/hill/107-tulare_entry_times.csv" );
    std::string line;
    int x = 0;
    while(std::getline(infile,line)) {
      std::stringstream lineStream(line);
      std::string cell;
      while(std::getline(lineStream,cell,' ')) {
        entry_times.push_back(std::stoi(cell));
      }
    }

    // print the pairs:
    //std::cout << std::endl;
    //std::cout << "There are " << pairs.get_num_pairs() << " persistence pairs: " << std::endl;
    for( phat::index idx = 0; idx < pairs.get_num_pairs(); idx++ ) {
        int birth = entry_times[pairs.get_pair( idx ).first];
        int death = entry_times[pairs.get_pair( idx ).second];
        if(death != birth) {
          std::cout << "Dimension: " << (int)boundary_matrix.get_dim(pairs.get_pair( idx ).first)<< ", Birth: " << birth << ", Death: " << death << ", Representative Cycle: ";
          std::vector< phat::index > temp_col;
          boundary_matrix.get_col( pairs.get_pair( idx ).second, temp_col );
          for( phat::index idx = 0; idx < (phat::index)temp_col.size(); idx++ ) {
              std::cout << " " << temp_col[ idx ];
          }
          std::cout << std::endl;

        }
      }

        /*
        // print some information of the boundary matrix:
        std::cout << std::endl;
        std::cout << "The boundary matrix has " << boundary_matrix.get_num_cols() << " columns: " << std::endl;
        for( phat::index col_idx = 0; col_idx < boundary_matrix.get_num_cols(); col_idx++ ) {
            std::cout << "Column " << col_idx << " represents a cell of dimension " << (int)boundary_matrix.get_dim( col_idx ) << ". ";
            if( !boundary_matrix.is_empty( col_idx ) ) {
                std::vector< phat::index > temp_col;
                boundary_matrix.get_col( col_idx, temp_col );
                std::cout << "Its boundary consists of the cells";
                for( phat::index idx = 0; idx < (phat::index)temp_col.size(); idx++ )
                    std::cout << " " << temp_col[ idx ];
            }
            std::cout << std::endl;

        }
        std::cout << "Overall, the boundary matrix has " << boundary_matrix.get_num_entries() << " entries." << std::endl;
        */
}
