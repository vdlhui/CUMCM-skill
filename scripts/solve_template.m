% solve_template.m — 通用 MATLAB 求解骨架
% 参数化设计 / 错误处理 / 运行日志 / 关键数值落盘

function main()
    fprintf('[%s] === CUMCM 求解开始 ===\n', datestr(now, 'HH:MM:SS'));

    try
        % === BEGIN MANAGED: modeling ===
        % 在此区域填入模型逻辑
        results = struct();
        % === END MANAGED: modeling ===

        save_results(results);
        fprintf('[%s] === 求解完成 ===\n', datestr(now, 'HH:MM:SS'));
    catch ME
        fprintf('[%s] !!! 求解失败: %s\n', datestr(now, 'HH:MM:SS'), ME.message);
        rethrow(ME);
    end
end

function data = load_data(data_dir)
    % 加载 P0 清洗后的数据
    data = struct();
    if exist(data_dir, 'dir')
        files = dir(fullfile(data_dir, '*.csv'));
        for i = 1:length(files)
            [~, name] = fileparts(files(i).name);
            data.(name) = readtable(fullfile(data_dir, files(i).name));
            fprintf('  已加载: %s\n', files(i).name);
        end
    end
end

function save_results(results, output_dir)
    if nargin < 2, output_dir = 'output'; end
    if ~exist(output_dir, 'dir'), mkdir(output_dir); end
    fprintf('结果已保存到: %s\n', output_dir);
end
