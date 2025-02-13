function [] = gen_24item_lists()
% generates trial lists with 24 trials per run

% create lists for each target dimension (north/south and west/east)
targDims = {'NS', 'WE'};
for dimIdx = 1:2
    thisTargDim = targDims{dimIdx}; % NS or WE
    
    % get three 16-trial blocks (fully balanced and randomized), which will
    % be grouped into two 24-trial runs.
    trials = generateTrialBlock; % returns 48 trials
    
    % divide into two runs
    assert(numel(trials)==48,'Unexpected number of trials');
    runTrials{1} = trials(1:24);
    runTrials{2} = trials(25:48);
    
    % save out the list for each run
    for rIdx = 1:2
        thisTrials = runTrials{rIdx};
        outfname = fullfile('new_24item_lists',sprintf('trialList_%s%d.csv',thisTargDim,rIdx));
                
        % get trial parameters in matrix form
        % params 1-4 are:
        %   (1) faces are attended?
        %   (2) faces are fearful?
        %   (3) attended stimuli match?  -> this determines the correct response
        %   (4) non-attended stimuli match?
        params = reshape([thisTrials.params],4,24)';
        
        % individual columns of the trial list        
        switch thisTargDim
            case 'NS'
                col_imgNorth = {thisTrials.attItem1}';
                col_imgSouth = {thisTrials.attItem2}';
                col_imgWest = {thisTrials.unAttItem1}';
                col_imgEast = {thisTrials.unAttItem2}';
            case 'WE'
                col_imgNorth = {thisTrials.unAttItem1}';
                col_imgSouth = {thisTrials.unAttItem2}';
                col_imgWest = {thisTrials.attItem1}';
                col_imgEast = {thisTrials.attItem2}';
        end
        col_iti = gen_itiCol;
        col_correctResponse = cell(24,1);
        col_correctResponse(params(:,3)>0.5) = {'IDENTICAL'};
        col_correctResponse(params(:,3)<0.5) = {'DIFFERENT'};
        col_targetDimension = repmat({thisTargDim},24,1);
        col_facesAreAttended = num2cell(params(:,1));
        col_facesAreFearful = num2cell(params(:,2));
        col_attendedItemsMatch = num2cell(params(:,3));
        col_nonAttendedItemsMatch = num2cell(params(:,4));
        
        % set up the structures to write out
        listArray = [col_imgNorth, col_imgSouth, col_imgWest, col_imgEast,...
            col_iti, col_correctResponse, col_targetDimension,...
            col_facesAreAttended, col_facesAreFearful,...
            col_attendedItemsMatch, col_nonAttendedItemsMatch];
        listHeaders = {'imgNorth', 'imgSouth', 'imgWest', 'imgEast',...
            'ITI', 'correctResponse', 'targetDimension',...
            'facesAreAttended', 'facesAreFearful',...
            'attendedItemsMatch', 'nonAttendedItemsMatch'};
        
        % write out the file
        fprintf('Writing file: %s\n\n',outfname);
        fid = fopen(outfname,'w');
        fprintf(fid,'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',listHeaders{:});
        listArray = listArray'; % transpose for output
        fprintf(fid,'%s,%s,%s,%s,%1.3f,%s,%s,%d,%d,%d,%d\n',listArray{:});
        fclose(fid);

    end % loop over runs
end % loop over target dimensions

end % end of main function


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% subfunction to generate a fully balanced 16-trial block
function [trialBlock] = generateTrialBlock()

    % it takes 16 trials to balance all 4 within-block parameters
    % the 4 parameters (each true/false) are:
    %   (1) faces are attended?
    %   (2) faces are fearful?
    %   (3) attended stimuli match?  -> this determines the correct response
    %   (4) non-attended stimuli match?
    nPerBlock = 16;

    % create a boolean matrix
    % 16 rows are trials, and 4 columns define the params above
    params(:,1) = [zeros(8,1); ones(8,1)];
    params(:,2) = repmat([zeros(4,1); ones(4,1)],2,1);
    params(:,3) = repmat([zeros(2,1); ones(2,1)],4,1);
    params(:,4) = repmat([0; 1],8,1);

    % randomize the rows AND repeat 3 times (tripling the length)
    % use a subfunction that constrains the number of times any given
    % condition value is repeated in the final permutation.
    params = randomizeBooleanRows(params);

    % initialize the stimulus pools
    % these will be used, together with the subfunction 'selectStim', to cycle
    % through stimulus items in random order without replacement. 
    itemPool.fearfulFaces = {};
    itemPool.neutralFaces = {};
    itemPool.houses = {};

    % loop over trials to insert specific stimulus items
    trialBlock = struct([]); % initialize
    for i = 1:(3*nPerBlock)

        % determine the attended and unattended stimulus type
        if params(i,2) % if faces are fearful
            faceType = 'fearfulFaces';
        else
            faceType = 'neutralFaces';
        end
        if params(i,1) % if faces are attended
            attItemType = faceType;
            unAttItemType = 'houses';
        else % if houses are attended
            attItemType = 'houses';
            unAttItemType = faceType;
        end

        % add stimulus items to the 'trials' struct
        % attended item 1
        [trialBlock(i).attItem1, itemPool] = selectItem(attItemType,itemPool);
        % attended item 2
        if params(i,3) % if the attended items match
            trialBlock(i).attItem2 = trialBlock(i).attItem1;
        else
            [trialBlock(i).attItem2, itemPool] = selectItem(attItemType,itemPool);
        end
        % unattended item 1
        [trialBlock(i).unAttItem1, itemPool] = selectItem(unAttItemType,itemPool);
        % unattended item 2
        if params(i,4) % if the unattended items match
            trialBlock(i).unAttItem2 = trialBlock(i).unAttItem1;
        else
            [trialBlock(i).unAttItem2, itemPool] = selectItem(unAttItemType,itemPool);
        end

        % also add parameters to the trials struct
        trialBlock(i).params = params(i,:);

    end

end % subfunction generateTrialBlock


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% subfunction to randamly permute rows of the condition matrix while
%%% constraining the number of successive repetitions
%%%
%%% in the output, the original params structure is repeated 3 times
%%% each is independently randomized, and repetitions are controlled across
%%% the entire output
function [paramsOut] = randomizeBooleanRows(params)

    % params is a boolean condition matrix (trials by parameters)
    
    % set the maximum number of times any given parameter value can be
    % repeated across consecutive trials
    maxNReps = 4;
    
    % repeatedly randomize until a qualifying order is found
    nTrials = size(params,1);
    nParams = size(params,2);
    ok = false;
    while ~ok
        paramsOut = [params(randperm(nTrials),:); params(randperm(nTrials),:); params(randperm(nTrials),:)];
        % loop over the individual parameters
        for i = 1:nParams
            ok = true;
            % find the trial indices where the parameter changes
            chgpts = find(diff([-1; paramsOut(:,i); -1])~=0);
            runLengths = diff(chgpts);
            if any(runLengths>maxNReps)
                ok = false;
                break
            end
        end % loop over the different parameters
    end % while loop
    
end % subfunction randomizeBooleanRows


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% subfunction to sample stimulus items in each category w/o replacement
function [item, itemPool] = selectItem(itemType,itemPool)

    % lists of all availabe stimulus items in the 3 types
    itemList.fearfulFaces = {
        'stimuli/Faces/F01.pict.jpg'
        'stimuli/Faces/F02.pict.jpg'
        'stimuli/Faces/F03.pict.jpg'
        'stimuli/Faces/F04.pict.jpg'
        'stimuli/Faces/F05.pict.jpg'
        'stimuli/Faces/F06.pict.jpg'
        'stimuli/Faces/F07.pict.jpg'
        'stimuli/Faces/F08.pict.jpg'
        'stimuli/Faces/F09.pict.jpg'
        'stimuli/Faces/F10.pict.jpg'
        };
    itemList.neutralFaces = {
        'stimuli/Faces/N01.pict.jpg'
        'stimuli/Faces/N02.pict.jpg'
        'stimuli/Faces/N03.pict.jpg'
        'stimuli/Faces/N04.pict.jpg'
        'stimuli/Faces/N05.pict.jpg'
        'stimuli/Faces/N06.pict.jpg'
        'stimuli/Faces/N07.pict.jpg'
        'stimuli/Faces/N08.pict.jpg'
        'stimuli/Faces/N09.pict.jpg'
        'stimuli/Faces/N10.pict.jpg'
        };
    itemList.houses = {
        'stimuli/Houses/H01.pict.jpg'
        'stimuli/Houses/H02.pict.jpg'
        'stimuli/Houses/H03.pict.jpg'
        'stimuli/Houses/H04.pict.jpg'
        'stimuli/Houses/H05.pict.jpg'
        'stimuli/Houses/H06.pict.jpg'
        'stimuli/Houses/H07.pict.jpg'
        'stimuli/Houses/H08.pict.jpg'
        'stimuli/Houses/H09.pict.jpg'
        'stimuli/Houses/H10.pict.jpg'
        'stimuli/Houses/H11.pict.jpg'
        'stimuli/Houses/H12.pict.jpg'
        'stimuli/Houses/H13.pict.jpg'
        'stimuli/Houses/H14.pict.jpg'
        'stimuli/Houses/H15.pict.jpg'
        'stimuli/Houses/H16.pict.jpg'
        'stimuli/Houses/H17.pict.jpg'
        'stimuli/Houses/H18.pict.jpg'
        'stimuli/Houses/H19.pict.jpg'
        'stimuli/Houses/H20.pict.jpg'
        };

    % if the item pool is empty, reset it (full list in random order)
    if isempty(itemPool.(itemType))
        nItems = numel(itemList.(itemType));
        itemPool.(itemType) = itemList.(itemType)(randperm(nItems));
    end
    
    % return the next item of the requested type
    item = itemPool.(itemType){1};
    itemPool.(itemType)(1) = [];
    
end % subfunction selectItem


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% subfunction to return a column of ITI durations for one run
function [itiCol] = gen_itiCol()

% the unique ITIs are:
% 	2.15, 4.66, 7.17, 9.68, 12.19
% 	i.e., 2.15 + 2.51*n, where n = [0, 1, 2, 3, 4]
% the number of trials per run with each value, respectively, is:
% 	10, 5, 3, 3, 3 -> 24 trials per run

% system:
%   -> last trial will always be given the shortest ITI
%       (no reason for a gap since nothing follows it)
%   -> remainder will be divided into 3 blocks with Ns as follows:
%       3, 2, 1, 1, 1
%       3, 1, 1, 1, 1
%       3, 2, 1, 1, 1
%   -> the order will be randomized within each block

% set up the possible ITI durations
itiVals = 2.15 + 2.51 * (0:4);

% set up the three successive blocks of trials
bk1 = [repmat(itiVals(1),1,3), repmat(itiVals(2),1,2), itiVals(3), itiVals(4), itiVals(5)];
bk2 = bk1;
bk2(4) = [];
bk3 = bk1;

% randomize and concatenate the blocks
itiCol = [bk1(randperm(8)), bk2(randperm(7)), bk3(randperm(8)), itiVals(1)]';

% convert to cell array
itiCol = num2cell(itiCol);

end % subfunction gen_itiCol



