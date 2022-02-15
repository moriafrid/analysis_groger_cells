% ----------------- Automatic, don't change (open/close etc) ------------%

function varargout = vis_neuron_fit_params(varargin)
    % VIS_NEURON_FIT_PARAMS MATLAB code for vis_neuron_fit_params.fig
    % Edit the above text to modify the response to help vis_neuron_fit_params
    % Last Modified by GUIDE v2.5 14-Feb-2022 15:52:26

    % Begin initialization code - DO NOT EDIT
    gui_Singleton = 1;
    gui_State = struct('gui_Name',       mfilename, ...
                       'gui_Singleton',  gui_Singleton, ...
                       'gui_OpeningFcn', @vis_neuron_fit_params_OpeningFcn, ...
                       'gui_OutputFcn',  @vis_neuron_fit_params_OutputFcn, ...
                       'gui_LayoutFcn',  [] , ...
                       'gui_Callback',   []);
    if nargin && ischar(varargin{1})
        gui_State.gui_Callback = str2func(varargin{1});
    end

    if nargout
        [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
    else
        gui_mainfcn(gui_State, varargin{:});
    end
    % End initialization code - DO NOT EDIT
end

function h_err_param_slider_CreateFcn(hObject, ~, handles)
    if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor',[.9 .9 .9]);
    end
end

function h_err_params_list_CreateFcn(hObject, ~, handles)
    if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
        set(hObject,'BackgroundColor','white');
    end
end

function h_errors_list_CreateFcn(hObject, eventdata, handles)
% hObject    handle to h_errors_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
end

function varargout = vis_neuron_fit_params_OutputFcn(hObject, ~, handles)
    varargout{1} = handles.output;
end

% ----------------- Adjusting GUI openning (open/close etc) ------------%

function vis_neuron_fit_params_OpeningFcn(hObject, ~, handles, varargin)
    % --- Executes just before vis_neuron_fit_params is made visible.
    % This function has no output args, see OutputFcn.
    % hObject    handle to figure
    % handles    structure with handles and user data (see GUIDATA)
    % varargin   command line arguments to vis_neuron_fit_params (see VARARGIN)

    global db;

    % Choose default command line output for vis_neuron_fit_params
    handles.output = hObject;
    
    db.filename = ask_for_filename(handles);
    db.simulation_results = load_csv_data(db.filename);
    
    db_options = fieldnames(db.simulation_results);
    for ignore = ["Properties", "Variables", "Row"]
        db_options = db_options(arrayfun(@(curr) isempty(strfind(curr{1}, ignore)), db_options));
    end
    params_list = db_options(arrayfun(@(curr) isempty(strfind(curr{1}, "error_")), db_options));
    err_list = db_options(arrayfun(@(curr) ~isempty(strfind(curr{1}, "error_")), db_options));
    handles.h_err_params_list.String = params_list;
    handles.h_errors_list.String = err_list;

    % Update handles structure
    guidata(hObject, handles);

    % UIWAIT makes vis_neuron_fit_params wait for user response (see UIRESUME)
    % uiwait(handles.figure1);
end

function figure1_DeleteFcn(hObject, eventdata, handles)
% hObject    handle to figure1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    clear db;
end

function result = ask_for_filename(handles)
    result = "";
    [f_name, p_name] = uigetfile({'*.csv'}, 'Choose simulation_result file');
    if p_name == 0
        msgbox('You must choose new data','Choose file','error');
        close(handles.figure1);  % todo are you sure? can just disable gui
        return
    end
    
    result = fullfile(p_name, f_name);
end

function simulation_results = load_csv_data(filename)
    arguments
        filename {mustBeFile};
    end
    opts = delimitedTextImportOptions("NumVariables", 7);

    % Specify range and delimiter
    opts.DataLines = [2, Inf];
    opts.Delimiter = ",";

    % Specify column names and types
    opts.VariableNames = ["CM", "RM", "RA", "RA0", "error_decay", "error_percentage", "error_rmsd"];
    opts.VariableTypes = ["double", "double", "double", "double", "double", "double", "double"];

    % Specify file level properties
    opts.ExtraColumnsRule = "ignore";
    opts.EmptyLineRule = "read";

    simulation_results = readtable(filename, opts);
end

% ----------------- Adjusting GUI callbacks (open/close etc) ------------%

function h_err_param_slider_Callback(hObject, ~, handles)
% --- Executes on slider movement.
% hObject    handle to h_err_param_slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider
    disp(append("Slider ", num2str(get(hObject,'Value'))))
end

function h_err_params_list_Callback(hObject, ~, handles)
% --- Executes on selection change in h_err_params_list.
% hObject    handle to h_err_params_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns h_err_params_list contents as cell array
%        contents{get(hObject,'Value')} returns selected item from h_err_params_list

    options_list = cellstr(get(hObject,'String'));
    disp(append("Param ", options_list(get(hObject,'Value'))));
end

function h_errors_list_Callback(hObject, eventdata, handles)
% hObject    handle to h_errors_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns h_errors_list contents as cell array
%        contents{get(hObject,'Value')} returns selected item from h_errors_list
end

