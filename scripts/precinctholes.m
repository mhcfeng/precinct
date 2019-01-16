function precinctholes(precinct)
    import edu.stanford.math.plex4.*;
    centroiddir='../data/extractcentroids/';
    filename=strcat(centroiddir,precinct,'.csv')
    precinctdata=csvread(filename,1,1);
    total=precinctdata(:,1)+precinctdata(:,2);
    hillpref=precinctdata(:,1)-precinctdata(:,2);
    hill=[precinctdata(hillpref>0,3),precinctdata(hillpref>0,4)];
    trump=[precinctdata(hillpref<0,3),precinctdata(hillpref<0,4)];
   
    max_dimension=2;
    coord=[precinctdata(:,3), precinctdata(:,4)];
    max_filtration_value=mean(pdist(coord))
    
    persistence=api.Plex4.getModularSimplicialAlgorithm(max_dimension,2);
 
    outputdir='../data/intervals/';
    hilloutfilename=strcat(outputdir,'hill/',precinct,'.csv');
    
    headers={'Group','Order','X','Y','Length','Start','End'};

    length(hill)
    if(and(~isempty(hill),length(hill)<10000))
        hilloutfilename
        hillstream=api.Plex4.createVietorisRipsStream(hill,max_dimension,max_filtration_value);
        hillintervals=persistence.computeAnnotatedIntervals(hillstream);
        hillintervalsmat=edu.stanford.math.plex4.homology.barcodes.BarcodeUtility.getEndpoints(hillintervals,1,0);
        
        if(~isempty(hillintervalsmat))
            hilldim1=hillintervals.getIntervalGeneratorPairsAtDimension(1);
            hillpairs=cell2mat(hilldim1.toArray.cell);
            hillgens=extractvertices(hillpairs);
            intervallength=hillintervalsmat(:,2)-hillintervalsmat(:,1);
            pathcoords=[];
            for i=[1:length(intervallength)]
                temp=hill(hillgens{i}+1,:);
                temp=[temp;temp(1,:)];
                temp=[repmat(i,size(temp,1),1),[1:size(temp,1)]',temp,repmat(intervallength(i),size(temp,1),1),repmat(hillintervalsmat(i,:),size(temp,1),1)];
                pathcoords=[pathcoords;temp];
            end

            csvwrite_with_headers(hilloutfilename,pathcoords,headers);
        end
        %save(hilloutfilename,'pathcoords');
    end
    
    trumpoutfilename=strcat(outputdir,'trump/',precinct,'.csv');
    
    length(trump)
    if(and(~isempty(trump),length(trump)<10000))
        trumpoutfilename
        trumpstream=api.Plex4.createVietorisRipsStream(trump,max_dimension,max_filtration_value);
        trumpintervals=persistence.computeAnnotatedIntervals(trumpstream);
        trumpintervalsmat=edu.stanford.math.plex4.homology.barcodes.BarcodeUtility.getEndpoints(trumpintervals,1,0);

        if(~isempty(trumpintervalsmat))
    
            trumpdim1=trumpintervals.getIntervalGeneratorPairsAtDimension(1);
            trumppairs=cell2mat(trumpdim1.toArray.cell);
            trumpgens=extractvertices(trumppairs);
        
            intervallength=trumpintervalsmat(:,2)-trumpintervalsmat(:,1);
            pathcoords=[];
            for i=[1:length(intervallength)]
                temp=trump(trumpgens{i}+1,:);
                temp=[temp; temp(1,:)];
                temp=[repmat(i,size(temp,1),1),[1:size(temp,1)]',temp,repmat(intervallength(i),size(temp,1),1),repmat(trumpintervalsmat(i,:),size(temp,1),1)];
                pathcoords=[pathcoords;temp];
            end
        
            csvwrite_with_headers(trumpoutfilename,pathcoords,headers);
        end
        %save(trumpoutfilename,'pathcoords');
    end
        
end
