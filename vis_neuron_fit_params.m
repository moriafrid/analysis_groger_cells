% ----------------- Automatic, don't change (open/close etc) ------------%

function varargout = vis_neuron_fit_params(varargin)
    % VIS_NEURON_FIT_PARAMS MATLAB code for vis_neuron_fit_params.fig
    % Edit the above text to modify the response to help vis_neuron_fit_params
    % Last Modified by GUIDE v2.5 14-Feb-2022 21:27:21

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

function h_err_params_2nd_list_CreateFcn(hObject, eventdata, handles)
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
    handles.h_err_params_2nd_list.String = params_list;
    handles.h_errors_list.String = err_list;
    
    update_plot(handles); % plot things

    % Update handles structure
    guidata(hObject, handles);

    % UIWAIT makes vis_neuron_fit_params wait for user response (see UIRESUME)
    % uiwait(handles.figure1);
end

function figure1_DeleteFcn(~, ~, handles)
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

function update_plot(handles)
    global db;
    
    h_ax = handles.h_ax_err_landscape;
    
    options_list = cellstr(handles.h_err_params_list.String);
    fieldname_1 = options_list(handles.h_err_params_list.Value);
    options_list = cellstr(handles.h_err_params_2nd_list.String);
    fieldname_2 = options_list(handles.h_err_params_2nd_list.Value);
    options_list = cellstr(handles.h_errors_list.String);
    fieldname_err = options_list(handles.h_errors_list.Value);
    
    is_2d = strcmp(fieldname_1{:}, fieldname_2{:});
    if isempty(h_ax.Children) || ~isfield(handles, 'h_scatter')
        if ~isfield(handles, 'h_scatter')
            cla(h_ax);
        end
        if is_2d
            handles.h_scatter = scatter(h_ax, ...
                db.simulation_results.(fieldname_1{:}), ...
                db.simulation_results.(fieldname_err{:}));
            h_ax.XLabel.String = fieldname_1{:};
            h_ax.YLabel.String = strrep(fieldname_err{:}, "_", " ");
            handles.h_rotate_checkbox.Enable = "off";
        else
            handles.h_scatter = scatter3(h_ax, ...
                db.simulation_results.(fieldname_1{:}), ...
                db.simulation_results.(fieldname_2{:}), ...
                db.simulation_results.(fieldname_err{:}));
            h_ax.XLabel.String = fieldname_1{:};
            h_ax.YLabel.String = fieldname_2{:};
            h_ax.ZLabel.String = strrep(fieldname_err{:}, "_", " ");
            handles.h_rotate_checkbox.Enable = "on";
        end
    else
        if (is_2d && ~isempty(handles.h_scatter.ZData))
            handles.h_scatter.ZData = [];          
        end
        handles.h_scatter.XData = db.simulation_results.(fieldname_1{:});
        h_ax.XLabel.String = fieldname_1{:};
        if is_2d
            handles.h_scatter.YData = db.simulation_results.(fieldname_err{:});
            h_ax.View = [0 90];  % 2d view (flat)
            h_ax.YLabel.String = strrep(fieldname_err{:}, "_", " ");
            handles.h_rotate_checkbox.Enable = "off";
        else
            handles.h_scatter.YData = db.simulation_results.(fieldname_2{:});
            handles.h_scatter.ZData = db.simulation_results.(fieldname_err{:});
            h_ax.View = [-37.5  30];  % 3d view
            h_ax.YLabel.String = fieldname_2{:};
            h_ax.ZLabel.String = strrep(fieldname_err{:}, "_", " ");
            handles.h_rotate_checkbox.Enable = "on";
        end
    end
    
    enable_disable_rotation(handles);
    guidata(handles.output, handles);
end

function enable_disable_rotation(handles)
    if handles.h_rotate_checkbox.Value  % true when checked
        rotate3d(handles.h_ax_err_landscape, 'on');
    else
        rotate3d(handles.h_ax_err_landscape, 'off');
    end
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

function h_err_params_list_Callback(~, ~, handles)
% --- Executes on selection change in h_err_params_list.
% hObject    handle to h_err_params_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    update_plot(handles);
end

function h_errors_list_Callback(~, ~, handles)
    % hObject    handle to h_errors_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    update_plot(handles);
end

function h_err_params_2nd_list_Callback(~, ~, handles)
    % hObject    handle to h_err_params_2nd_list (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    update_plot(handles);
end

function h_rotate_checkbox_Callback(~, ~, handles)
    % hObject    handle to h_rotate_checkbox (see GCBO)
    % eventdata  reserved - to be defined in a future version of MATLAB
    % handles    structure with handles and user data (see GUIDATA)

    enable_disable_rotation(handles);
end