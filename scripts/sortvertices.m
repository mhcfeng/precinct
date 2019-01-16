function vertexorder=sortvertices(vertices)
    numpairs=size(vertices,1);
    vertexorder=[];
    vertexorder=[vertexorder,vertices(1,:)];
    vertices=vertices(2:end,:);
    for i=[1:numpairs-2]
        last=vertexorder(end);
        [row,col]=find(vertices==last);
        next = vertices(row,mod(col,2)+1);
        vertices(row,:)=[];
        vertexorder=[vertexorder,next];
    end
end