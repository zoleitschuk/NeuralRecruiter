function [feature_matrix] = data_convert()
	data = loadjson("new_job_desc.JSON");
	
	data_fields = fieldnames(data);
	
	n = numel(data_fields);
	
	feature_matrix = [];
	
	for i=1:n
		posting_text = data.(data_fields{i});
		posting_indices = processEmail(posting_text);
		posting_features = emailFeatures(posting_indices);
		feature_matrix = [feature_matrix; posting_features'];
		
		fprintf('%d of %d postings completed...', i, n);
	end