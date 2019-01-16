function vertices=extractvertices(annotated)
    vertices={};
    for i=[1:length(annotated)]
        formalsum=get(annotated(i),'Second');
        simplex=edu.stanford.math.plex4.utility.FormalSumUtility.extractActiveBasisElements(formalsum);
        vertices{i}= sortvertices(edu.stanford.math.plex4.utility.FormalSumUtility.extractVertices(simplex));
    end
end