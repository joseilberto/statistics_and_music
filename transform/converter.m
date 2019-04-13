function convert_midi_to_csv = converter(midi_file, output_file, miditoolbox_path)
warning('off')
addpath(miditoolbox_path)
midi_to_data = readmidi(midi_file);
cheader = {'t_beats' 'DeltaT_beats' 'channel' 'note_number' 'loudness' 't_seconds' 'DeltaT_seconds'};
commaheader = [cheader;repmat({','},1,numel(cheader))];
commaheader = commaheader(:)';
textheader = cell2mat(commaheader);
textheader = textheader(end, 1:end-1);
fid = fopen(output_file, "w");
fprintf(fid, "%s\n", textheader);
fclose(fid);
dlmwrite(output_file, midi_to_data, '-append');
end
