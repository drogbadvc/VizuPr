<?php
$myPDO = new PDO('sqlite:spider.sqlite');

$result = $myPDO->query("SELECT COUNT(from_id) AS inbound, from_id, to_id, Pages.url, Pages.new_rank 
FROM links JOIN Pages ON links.to_id = Pages.id 
GROUP BY to_id ORDER BY min(from_id)")->fetchAll();

$website = $myPDO->query("SELECT COUNT(from_id) AS inbound, from_id, to_id, Pages.url, Pages.new_rank 
FROM links JOIN Pages ON links.to_id = Pages.id WHERE Pages.id = 1")->fetch();

$va = '';
$arr_data = [['id', 'parentId', 'size'], [$website['url'], '', $website['inbound']]];

foreach ($result as $key => $value) {
    foreach ($result as $k => $v) {
        if ($value['from_id'] == $v['to_id']) {
            $va = $v['url'];
        }
    }
    if ($value['url'] != $va) {
        $arr_data[] = [$value['url'], $va, $value['inbound']];
    }
}

$filename = 'data.csv';

$handle = fopen('public/data.csv', 'w');

foreach ($arr_data as $fields) {
    fputcsv($handle, $fields);
}